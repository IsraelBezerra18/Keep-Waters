import json


class Save:
    def __init__(self) -> None:
        # with open("save.json", "r+") as file:
        #     pass
        self.__save_padrao = {
            'config': {
                'resolucoes_disponiveis': ((800, 600), (1024, 768), (1280, 720), (1360, 768), 
                                           (1366, 768), (1920, 1080), 'automático'),
                'resolucao_tela': (1280, 720),
                'get_fps': False,
                'limite_fps': 1000,
                'musica': True,
                'volume_musica': 1,
                'volume_jogo': 1,
            },
            'save': {
                'nome': None,
                'pdp': 0,
                'valores': {
                    'player': {
    
                        'posMap': [], 
                        'genero': 'masculino'
                    },
                    'residuos': {},
                    'pos_mapa': []
                }
            }
        }
        self.config = self.__save_padrao['config']
        self.save_id = 0
        self.pasta = "save"

    def new_save(self, nome):
        setattr(self, nome, self.__save_padrao['save'])
        with open(f"{self.pasta}/{nome}_{self.save_id}", "w") as save:
            json.dump(self.__save_padrao["save"], save)
            self.save_id += 1
