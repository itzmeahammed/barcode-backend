from flask import request, jsonify
from Models.attendance_model import Attendance
from Models.user_model import User
from Utils.CommonExceptions import CommonException
from datetime import datetime
import logging

class AttendanceController:
    def markAttendance():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token, role='employee').first()
            if not user:
                return CommonException.InvalidIdException()

            status = request.json.get('status')
            if status not in ['present', 'absent','leave']:
                return jsonify({"message": "Invalid status"}), 400

            today = datetime.now().date()
            existing_record = Attendance.objects(employee=user, data__gte=today).first()
            if existing_record:
                return jsonify({"message": "Attendance already marked for today"}), 400

            attendance = Attendance(employee=user, status=status)
            attendance.save()

            return jsonify({
                "message": "Attendance marked successfully",
                "attendance": attendance.to_json()
            }), 200
        except Exception as e:
            logging.error(f"Error in markAttendance: {str(e)}")
            return CommonException.handleException(e)
    
    def markAttendanceAbsent():
        try:
            status = request.json.get('status')
            user = request.json.get('user')
            if status not in ['present', 'absent','leave']:
                return jsonify({"message": "Invalid status"}), 400
            
            today = datetime.now().date()
            existing_record = Attendance.objects(employee=user, data__gte=today).first()
            if existing_record:
                return jsonify({"message": "Attendance already marked for today"}), 400

            
            attendance = Attendance(employee=user, status=status)
            attendance.save()

            return jsonify({
                "message": "Attendance marked successfully",
                "attendance": str(attendance.id)
            }), 200
        except Exception as e:
            logging.error(f"Error in markAttendanceAbsent: {str(e)}")
            return CommonException.handleException(e)

    def updateAttendance():
        try:
            attendance_id = request.args.get("id")
            if not attendance_id:
                return CommonException.IdRequiredException()

            status = request.json.get('status')
            if status not in ['present', 'absent','leave']:
                return jsonify({"message": "Invalid status"}), 400

            attendance = Attendance.objects(id=attendance_id).first()
            if not attendance:
                return CommonException.InvalidIdException()

            attendance.update(status=status)
            return jsonify({"message": "Attendance updated successfully"}), 200
        except Exception as e:
            logging.error(f"Error in updateAttendance: {str(e)}")
            return CommonException.handleException(e)

    def getTodayAttendance():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token, role='employee').first()
            if not user:
                return CommonException.InvalidIdException()

            today = datetime.now().date()
            attendance = Attendance.objects(employee=user, data__gte=today).first()

            if attendance:
                return jsonify(attendance.to_json()), 200
            else:
                return jsonify({"message": "No attendance marked for today"}), 404
        except Exception as e:
            logging.error(f"Error in getTodayAttendance: {str(e)}")
            return CommonException.handleException(e)

    def getEmployeeAttendance():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token, role='employee').first()
            if not user:
                return CommonException.InvalidIdException()

            records = Attendance.objects(employee=user)
            return jsonify([a.to_json() for a in records]), 200
        except Exception as e:
            logging.error(f"Error in getEmployeeAttendance: {str(e)}")
            return CommonException.handleException(e)
    
    def getAllEmployeeAttendance():
        try:
            query = request.args.to_dict()
            if query:
                records = Attendance.objects(**query)
            else:
                records = Attendance.objects()
            return jsonify([a.to_json() for a in records]), 200
        except Exception as e:
            logging.error(f"Error in getAllEmployeeAttendance: {str(e)}")
            return CommonException.handleException(e)

    def deleteAttendance():
        try:
            attendance_id = request.args.get("id")
            if not attendance_id:
                return CommonException.IdRequiredException()

            attendance = Attendance.objects(id=attendance_id).first()
            if not attendance:
                return CommonException.InvalidIdException()

            attendance.delete()
            return jsonify({"message": "Attendance deleted successfully"}), 200
        except Exception as e:
            logging.error(f"Error in deleteAttendance: {str(e)}")
            return CommonException.handleException(e)
