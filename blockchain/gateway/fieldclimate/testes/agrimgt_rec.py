# https://github.com/agrimgt/python-fieldclimate
# recommended

from asyncio import gather, run
from fieldclimate import FieldClimateClient

async def main():
    async with FieldClimateClient(
        private_key="ec07663127f0f862d2fd91d32251b3667fde7c479cf3fd00",
        public_key="0b0989163ed6b703cd13904039b4731bea2788e76f51e20f",
        connections=20
    ) as client:
        async def print_user_json():
            print(await client.get_user())

        async def print_station_dates(station):
            print(await client.get_data_range(station))

        async def count_stations_then_print_ranges():
            stations = await client.get_user_stations()
            print(len(stations))
            await gather(*[
                print_station_dates(station)
                for station in stations[:10]
            ])

        await gather(
            print_user_json(),
            count_stations_then_print_ranges(),
        )

if __name__ == "__main__":
    run(main())