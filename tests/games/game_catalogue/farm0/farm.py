import os

from tests.games.game_agents.basic_agents import Farmgym_RandomAgent
from tests.games.game_builder.make_farm import make_farm
from tests.games.game_builder.run_farm import run_gym_xp

from farmgym.v2.rendering.monitoring import make_variables_to_be_monitored


def env():
    yaml_path = os.path.join(os.path.dirname(__file__), "farm0.yaml")
    farm = make_farm(yaml_path)

    farm.add_monitoring(
        make_variables_to_be_monitored(
            [
                "f0>weather>rain_amount#mm.day-1",
                "f0>weather>clouds#%",
                "f0>weather>air_temperature>mean#°C",
                "f0>weather>wind>speed#km.h-1",
                "f0>soil>available_Water#L",
                "f0>soil>microlife_health_index#%",
                # "f0>plant>size#cm",
                # "f0>plant>cumulated_water#L",
                # "f0>plant>cumulated_stress_water#L",
                # "f0>plant>flowers_per_plant#nb@mat",
                # "f0>plant>flowers_per_plant#nb"
            ]
        )
    )

    return farm


if __name__ == "__main__":
    f = env()
    print(f)
    agent = Farmgym_RandomAgent()
    run_gym_xp(f, agent, max_steps=150, render="text")
