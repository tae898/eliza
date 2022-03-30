import time

import jsonpickle
import python_on_whales
import requests


def start_docker_container(
    image: str, port_id: int, sleep_time=5
) -> python_on_whales.Container:
    """Start docker container given the image name and port number.

    Args
    ----
    image: docker image name
    port_id: port id
    sleep_time: warmup time

    Returns
    -------
    container: a docker container object.

    """
    print(f"starting a docker container ... {image}")
    container = python_on_whales.docker.run(
        image=image, detach=True, publish=[(port_id, port_id)]
    )

    time.sleep(sleep_time)

    return container


def kill_container(container: python_on_whales.Container) -> None:
    """Kill docker container.

    Args
    ----
    container: a docker container object.

    """
    print(f"killing {container} ...")
    container.kill()


def recognize_emotion(utterance: str, url_erc: str = "http://127.0.0.1:10006") -> str:
    """Recognize the speaker emotion of a given utterance.

    Args
    ----
    utterance:
    url_erc: the url of the emoberta api server.

    Returns
    -------
    emotion

    """
    data = {"text": utterance}

    data = jsonpickle.encode(data)
    response = requests.post(url_erc, json=data)
    response = jsonpickle.decode(response.text)
    emotion = max(response, key=response.get)

    return emotion
