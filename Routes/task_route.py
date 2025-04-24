from Controllers.task_controller import TaskController
from flask import Blueprint

task_bp = Blueprint('Task', __name__)

task_bp.add_url_rule('/getAlltask', view_func=TaskController.getAllTasks, methods=['GET'])
task_bp.add_url_rule('/getTaskByRole', view_func=TaskController.getTasksByUser, methods=['GET'])
task_bp.add_url_rule('/createTask', view_func=TaskController.createTask, methods=['POST'])
task_bp.add_url_rule('/updateTask', view_func=TaskController.updateTask, methods=['PUT'])
task_bp.add_url_rule('/deleteTask', view_func=TaskController.deleteTask, methods=['DELETE'])
