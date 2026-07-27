from flask import Flask, jsonify, request
from flask_cors import CORS

from minesweeper import Board
from solver import Solver

