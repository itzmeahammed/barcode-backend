from flask import Blueprint
from Controllers.attendance_controller import AttendanceController

attendance_bp = Blueprint('attendance_bp', __name__)

attendance_bp.route('/mark', methods=['POST'])(AttendanceController.markAttendance)
attendance_bp.route('/markAbsent', methods=['POST'])(AttendanceController.markAttendanceAbsent)
attendance_bp.route('/update', methods=['PUT'])(AttendanceController.updateAttendance)
attendance_bp.route('/today', methods=['GET'])(AttendanceController.getTodayAttendance)
attendance_bp.route('/employee', methods=['GET'])(AttendanceController.getEmployeeAttendance)
attendance_bp.route('/getAll', methods=['GET'])(AttendanceController.getAllEmployeeAttendance)
attendance_bp.route('/delete', methods=['DELETE'])(AttendanceController.deleteAttendance)
