import requests
import argparse
import glob
import time
import os
import json
from dataclasses import dataclass

BASE_URL = "https://bdl.stat.gov.pl/api/v1/"

class NoResourceException(Exception):
    pass

class APIErrorException(Exception):
    pass

class BrokenDataPoint(Exception):
    pass


@dataclass(eq=True, unsafe_hash=True)
class DataEntry:
    data: tuple
    start_year: int
    end_year: int
    name: str
    topic: str
    region: str
    unit: str
    res_id: int = -1

    def save(self, prefix):
        folder_path = os.path.join(prefix, str(self.res_id))
        os.makedirs(folder_path, exist_ok=True)

        fname = os.path.join(folder_path, f"{self.region}.json")
        with open(fname, 'w') as file:
            json.dump(self.__dict__, file)

    def get_range(self, start, end):
        if start < self.start_year or end > self.end_year or start > end:
            raise ValueError("Incorrect range boundries")
        if end == self.end_year:
            alt_data = self.data[start - self.start_year :]

        else:
            alt_data = self.data[start - self.start_year : end - self.end_year]

        return DataEntry(
            alt_data,
            start,
            end,
            self.name,
            self.topic,  
            self.region,
            self.unit,
            self.res_id
        )
    
    @classmethod
    def from_json(cls, fp):
        d = json.load(fp)
        d['data'] = tuple(d['data'])
        return cls(**d)


class DataCollection:

    def __init__(self):

        self.set_dict = {i: set() for i in range(1980, 2020)}
    
    def add(self, entry: DataEntry):
        for y in range(entry.start_year, entry.end_year):
            self.set_dict[y].add(entry)

    def return_range(self, start, stop):
        result = self.set_dict[start]
        for y in range(start, stop):
            result &= self.set_dict[y]
        return [e.get_range(start, stop) for e in result]

    @classmethod
    def read(cls, directory):
        result = cls()
        for fname in glob.glob(os.path.join(directory, '*/*')):
            with open(fname) as file:
                e = DataEntry.from_json(file)
                result.add(e)
        return result


class BdlApi:

    def __init__(self, token=None):
        """This is where authentication will be some day"""
        self._s = requests.session()
        self.__token = token
        self.subject_memoizer = {}


    def get_subject(self, subject_id):
        """recursively finds full subject (including parents) of given id. Costs up to ±4 queries. Memoized."""
        q = self.subject_memoizer.get(subject_id)
        if q:  # we already have this subject
            return q
        data = self._api_query(f"Subjects/{subject_id}").json()
        parent_id = data.get('parentId')
        name = data["name"]
        if parent_id is None:
            self.subject_memoizer[subject_id] = name
            return name
        else:
            result = f"{self.get_subject(parent_id)} - {name}"
            self.subject_memoizer[subject_id] = result
            return result

    def fetch_data_point(self, var_id):

        var_data = self._api_query(f"Variables/{var_id}").json()

        name = ""
        i = 1
        while True:
            next_segment = var_data.get(f"n{i}")
            if next_segment is None:
                break
            else:
                if i != 1:
                    name += " - "
                name += next_segment
                i += 1
        
        y_start = var_data['years'][0]
        y_end = var_data['years'][-1] + 1

        if len(var_data['years']) != y_end - y_start:
            raise BrokenDataPoint

        unit = var_data['measureUnitName']

        subject = self.get_subject(var_data["subjectId"])

        raw_results = []
        result = []
        r_polska = self._api_query(f"data/by-variable/{var_id}", year=list(range(1990, 2020)), **{'unit-level': 0})
        r_voivodships = self._api_query(f"data/by-variable/{var_id}", year=list(range(1990, 2020)), **{'unit-level': 2, 'page-size': 20})
        raw_results.extend(r_polska.json()['results'])
        raw_results.extend(r_voivodships.json()['results'])

        for e in raw_results:
            result.append(DataEntry(
                [i['val'] for i in e['values']],
                y_start,
                y_end,
                name,
                subject,
                e['name'],  # region name
                unit,
                var_id
            ))

        return result


    def _api_query(self, query, **kwargs):
        kwargs['format'] = 'json'

        headers = {}
        if self.__token:
            headers['X-ClientId'] = self.__token

        r = self._s.get(BASE_URL + query, headers=headers, params=kwargs)
        if r.status_code == 200:
            return r
        elif r.status_code == 404:
            raise NoResourceException(f"{query} returned 404")
        else:
            raise APIErrorException(f"{r.text}")

if __name__ == "__main__":
    token = open('token.txt').read().strip('\n')
    b = BdlApi(token)

    PREFIX = 'data3'
    t0 = time.time()
    counter = 0
    prev = time.time()
    for i in range(3001, 30000, 3):
        try:
            things = b.fetch_data_point(i)
        except NoResourceException:
            print(f"404: {i}")
            pass
        except BrokenDataPoint:
            print(f"Broken datapoint {i}")
        except APIErrorException as exception:
            print(repr(exception))
            time.sleep(10)
        for e in things:
            e.save(PREFIX)
        
        counter += 1
        speed = counter / (time.time() - t0) * 60
        print(f'Query finished after {time.time() - prev}s     {speed:.2}/min')
        prev = time.time()
        


