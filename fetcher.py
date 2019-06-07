import requests
import time
import os
import json
from dataclasses import dataclass

BASE_URL = "https://bdl.stat.gov.pl/api/v1/"

class NoResourceException(Exception):
    pass

class APIErrorException(Exception):
    pass

def api_time_string(start, stop):
    result = ''
    for y in range(start, stop - 1):
        result += f'year={y}&'
    result += f'year={stop -1}'
    return result


@dataclass
class DataEntry:
    data: list
    start_year: int
    end_year: int
    name: str
    region: str
    unit: str
    res_id: int = -1

    def save(self, prefix):
        folder_path = os.path.join(prefix, str(self.res_id))
        os.makedirs(folder_path, exist_ok=True)

        fname = os.path.join(folder_path, f"{self.region}.json")
        with open(fname, 'w') as file:
            json.dump(self.__dict__, file)
    
    @classmethod
    def from_json(cls, fp):
        return cls(**json.load(fp))


class DataCollection:

    def __init__(self):

        self.set_dict = {i: set() for i in range(1980, 2020)}
    
    def add(self, entry: DataEntry):
        for y in range(entry.start_year, entry.end_year + 1):
            self.set_dict[y].add(entry)

    def return_range(self, start, stop):
        result = self.set_dict[start]
        for y in range(start, stop):
            result &= self.set_dict[y]
        return result

class BdlApi:

    def __init__(self, token=None):
        """This is where authentication will be some day"""
        self._s = requests.session()
        self.__token = token

    def fetch_data_point(self, var_id):

        var_data = self._api_query(f"Variables/{var_id}").json()

        name = var_data['n1']
        name2 = var_data.get('n2')
        if name2:
            name += name2
        
        y_start = var_data['years'][0]
        y_end = var_data['years'][-1]

        unit = var_data['measureUnitName']

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
                e['name'],
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

    PREFIX = 'data'
    t0 = time.time()
    counter = 0
    prev = time.time()
    for i in range(1000, 30000):
        try:
            things = b.fetch_data_point(i)
        except NoResourceException:
            pass
        except APIErrorException as exception:
            print(repr(exception))
            time.sleep(1)
        for e in things:
            e.save(PREFIX)
        
        counter += 1
        speed = counter / (time.time() - t0) * 60
        print(f'Querry finished after {time.time() - prev}s     {speed:.2}/min')
        prev = time.time()
        


