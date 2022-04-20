from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
from flask_jwt_extended import jwt_required
import sqlite3


path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {chave: dados[chave]
                         for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            })

        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': f'Hotel id {hotel_id} already esxists.'}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        if not SiteModel.find_by_id(dados['site_id']):
            return {'message':'The hotel must be associated to a valid site id .'}, 400 # bad request
        hotel.save_hotel()
        return hotel.json()

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_enc = HotelModel.find_hotel(hotel_id)
        if hotel_enc:
            hotel_enc.update_hotel(**dados)
            if not SiteModel.find_by_id(dados['site_id']):
                return {'message':'The hotel must be associated to a valid site id .'}, 400 # bad request
            hotel_enc.save_hotel()
            return hotel_enc.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404
