import api_comunicator as api
import parser_ability
import argparse

import trainer

# Creamos el objeto ArgumentParser
parser = argparse.ArgumentParser(description='Creación de una APT inteligente para Mitre Caldera')

# Agregamos los argumentos que queremos recibir
parser.add_argument('-c', '--cookie', type=str, required=True, help='Valor de la cookie API_SESSION')
parser.add_argument('-p', '--platform', type=int, choices=range(0, 3), required=True, help='Plataforma sobre la que se va a dValor de la cookie API_SESSIONesarrollar la APT. 0:Linux; 1:Windows; 2:Darwin')
parser.add_argument('-ne', '--num_epochs', type=int, default=1000, help='Número de epochs durante las que se queire entrenar al modelo. Recomendable que el valor este entre 500 y 2000, dependiendo de la complejidad del problema')
parser.add_argument('-s', '--steps', type=int, choices=range(4, 11),required=True, help='Número de comandos que tiene que elegir el modelo en cada iteración. Este valor debe estar entre 4 y 10')
parser.add_argument('-e', '--evaluate', type=int, default=50, help='Cada cuántas epochs se debe evaluar el modelo')

# Parseamos los argumentos
args = parser.parse_args()

# Parseamos las habilidades de la plataforma seleccionada
def platform_translator(platform):

   

    dictionary_platform = {
        0: 'linux',
        1: 'windows',
        2: 'darwin'
    }

    # Creamos JSON con las habilidades de la plataforma seleccionada
    platform = dictionary_platform.get(platform)
    print("Seleccionadas habilidades de " + platform + "\n")
    return platform


# INICIO EJECUCIÓN
print("\n\nBIENVENIDO A INTELLIGENT APT\n\n")

# Cargamos todas las habilidades de Caldera
api = api.comunicator()
if(api.get_abilities(args.cookie)):
    print("Habilidades de Mitre Caldera cargadas\n")

    # Parseamos las habilidades obtenidas dependiendo de la plataforma seleccionada
    platform = platform_translator(args.platform)
    parser = parser_ability.parser()
    abilities = parser.filter_platform(platform)
    # Instanciamos el objeto que crea y entrena a la red neuronal
    trainer = trainer.Trainer(args.num_epochs,args.steps,abilities,500000) 
    action_sequence = trainer.train(args.evaluate)
    # Creamos la operación en CALDERA
    api.create_operation(args.cookie,action_sequence)
    print("APT INICIADA")
