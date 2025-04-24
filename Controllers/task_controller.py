from Models.task_model import Task
from Models.user_model import User
from flask import jsonify, request
from Utils.CommonExceptions import CommonException
from datetime import datetime
import logging


class TaskController:
    def getAllTasks():
        try:
            query = request.args.to_dict()
            if query:
                tasks = Task.objects(**query)
            else:
                tasks = Task.objects()
            return jsonify([task.to_json() for task in tasks]), 200
        except Exception as e:
            logging.error(f"Error in getAllTasks: {str(e)}")
            return CommonException.handleException()

    def getTasksByUser():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()

            if not user:
                return CommonException.InvalidIdException()

            if user.role == 'manager':
                tasks = Task.objects(manager=user.id)
            elif user.role == 'employee':
                tasks = Task.objects(employee=user.id)
            else:
                tasks = []

            return jsonify([task.to_json() for task in tasks]), 200
        except Exception as e:
            logging.error(f"Error in getTasksByUser: {str(e)}")
            return CommonException.handleException()

    def createTask():
        try:
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()

            token = request.headers.get('Authorization')
            manager = User.objects(auth_token=token, role='manager').first()
            if not manager:
                return CommonException.InvalidIdException()

            employee_id = data.get('employee')
            task = data.get('task')
            

            if not all([employee_id, task]):
                return CommonException.DataRequiredException()

            employee = User.objects(id=employee_id, role='employee').first()
            if not employee:
                return jsonify({"error": "Employee not found"}), 400

            new_task = Task(
                manager=manager,
                employee=employee,
                task=task,
            )
            new_task.save()
            return jsonify({"message": "Task Created Successfully", "task": str(new_task.id)}), 200
        except Exception as e:
            logging.error(f"Error in createTask: {str(e)}")
            return CommonException.handleException()

    def updateTask():
        try:
            task_id = request.args.get('id')
            if not task_id:
                return CommonException.IdRequiredException()

            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()

            task = Task.objects(id=task_id).first()
            if not task:
                return CommonException.InvalidIdException()

            data['updated_at'] = datetime.utcnow()
            task.update(**data)
            return jsonify({"message": "Task Updated Successfully"}), 200
        except Exception as e:
            logging.error(f"Error in updateTask: {str(e)}")
            return CommonException.handleException()

    def deleteTask():
        try:
            task_id = request.args.get('id')
            if not task_id:
                return CommonException.IdRequiredException()

            token = request.headers.get('Authorization')
            manager = User.objects(auth_token=token, role='manager').first()
            if not manager:
                return CommonException.InvalidIdException()

            task = Task.objects(id=task_id, manager=manager.id).first()
            if not task:
                return CommonException.InvalidIdException()

            task.delete()
            return jsonify({"message": "Task Deleted Successfully"}), 200
        except Exception as e:
            logging.error(f"Error in deleteTask: {str(e)}")
            return CommonException.handleException()
