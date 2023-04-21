import os
import re

from pathlib import Path


class TestDockerfileCompose:
    root_dir = Path(__file__).parent.parent.parent
    infra_dir_path = os.path.join(Path(__file__).parent.parent.parent, 'infra')


    def test_infra_structure(self):
        assert 'infra' in os.listdir(self.root_dir), (
            f'Проверьте, что в пути {self.root_dir} указана папка `infra`'
        )
        assert os.path.isdir(self.infra_dir_path), (
            f'Проверьте, что {self.infra_dir_path} - это папка, а не файл'
        )

    def test_docker_compose_file(self):
        try:
            with open(f'{os.path.join(self.infra_dir_path, "docker-compose.yml")}', 'r') as f:
                docker_compose = f.read()
        except FileNotFoundError:
            assert False, f'Проверьте, что в директорию {self.infra_dir_path} добавлен файл `docker-compose.yml`'

        assert re.search(r'image:\s+postgres:latest', docker_compose), (
            'Проверьте, что  в файл docker-compose.yaml добавлен образ postgres:latest'
        )
        assert re.search(r'image:\s+([a-zA-Z0-9]+)\/([a-zA-Z0-9_\.])+(\:[a-zA-Z0-9_-]+)?', docker_compose), (
            'Проверьте, что добавили сборку контейнера из образа на вашем DockerHub в файл docker-compose.yml'
        )
