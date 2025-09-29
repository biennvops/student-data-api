#!/usr/bin/env python3

import requests
import hashlib
import json
import os
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dotenv import load_dotenv
from checksum import checksum

load_dotenv()

class API:
    """
    Complete API client with all endpoints from the mobile app.
    """
    
    # Base URLs
    BASE_URL = os.getenv('BASE_URL')
    GOOGLE_AUTH_URL = os.getenv('GOOGLE_AUTH_URL')
    
    def __init__(self):
        # Load authentication key from environment variables
        self.AUTHEN_KEY = os.getenv('AUTHEN_KEY')
        if not self.AUTHEN_KEY:
            raise ValueError(
                "Missing required environment variable AUTHEN_KEY. "
                "Please set it in your .env file."
            )
        
        self.checksum = checksum()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'okhttp/3.12.1'
        })
    
    def _make_request(self, method: str, url: str, params: Optional[Dict] = None, 
                     data: Optional[Dict] = None, use_json: bool = True) -> Dict[str, Any]:
        """Make HTTP request with error handling."""
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                if use_json:
                    response = self.session.post(url, params=params, json=data)
                else:
                    response = self.session.post(url, params=params, data=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Parse JSON response if possible
            json_data = None
            try:
                json_data = response.json()
            except:
                pass
            
            # Determine success based on HTTP status and JSON response
            is_success = response.status_code == 200
            if json_data and 'code' in json_data:
                # API returns success info in JSON code field
                is_success = is_success and json_data['code'] == '200'
            return {
                'success': is_success,
                'status_code': response.status_code,
                'data': json_data,
                'raw_response': response.text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': None,
                'data': None
            }

    # Student Information APIs

    def get_student_by_id(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student information."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetStudentById"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def get_student_rate(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student rating information."""
        # TODO: 
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetStudentRate"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def add_rate(self, campus_code: str, authen: str, rate_id: str, 
                 rate_value: str, rate_comment: str) -> Dict[str, Any]:
        """Submit student rating."""
        checksum = self.checksum.checksum_k(rate_id, campus_code)
        
        url = f"{self.BASE_URL}/AddRate"
        params = {
            'campusCode': campus_code,
            'Authen': authen,
            'rateid': rate_id,
            'rateValue': rate_value,
            'rateComment': rate_comment,
            'checksum': checksum
        }
        
        return self._make_request('POST', url, params=params)
    
    def get_balance(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student account balance."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetBalance"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def get_fee_by_roll(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student fee information."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GeFeeByRoll"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def get_application(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student applications."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetApplication"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def retrieve_image(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Retrieve student profile image."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/RetriveImage"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    # Academic APIs
    
    def get_diemphongtrao(self, campus_code: str, roll_number: str, 
                         semester: str, authen: str) -> Dict[str, Any]:
        """Get extra-curricular points."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetDiemphongtrao"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'semester': semester,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    # Activity APIs
    
    def get_activity_student(self, campus_code: str, semester: str, 
                           roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student activities for a semester."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetActivityStudent"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Semester': semester,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def get_activity_student_by_week(self, campus_code: str, week: str, roll_number: str,
                                   semester: str, year: str, authen: str) -> Dict[str, Any]:
        """Get student activities for a specific week."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetActivityStudentByWeek"
        params = {
            'campusCode': campus_code,
            'week': week,
            'rollNumber': roll_number,
            'Semester': semester,
            'year': year,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    # Notification APIs
    
    def get_notification_by_roll(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Get notifications by roll number."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetNotificationByRoll"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    # System APIs
    
    def get_all_active_campus(self) -> Dict[str, Any]:
        """Get all active campus information."""
        url = f"{self.BASE_URL}/GetAllActiveCampus"
        return self._make_request('GET', url)
    
    def get_version(self) -> Dict[str, Any]:
        """Get API version information."""
        url = f"{self.BASE_URL}/GetVersion"
        return self._make_request('GET', url)
    
    def get_campus_info(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Get campus information."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/GetCampusInfo"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    # Feedback APIs
    
    def check_open_feedback(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Check if feedback is open."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/CheckOpenFeedBack"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def check_update_profile(self, campus_code: str, roll_number: str, authen: str) -> Dict[str, Any]:
        """Check if profile update is required."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        
        url = f"{self.BASE_URL}/CheckUpdateProfile"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def get_required_survey(self, username: str) -> Dict[str, Any]:
        """
        Get required survey information.
        Uses the Google authentication server.
        """
        checksum = self.checksum.checksum_y(username.lower().strip(), '')
        
        url = f"{self.GOOGLE_AUTH_URL}/GetRequiredSurvey"
        params = {
            'username': username.lower().strip(),
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    # Additional utility methods
    
    def get_semester(self, campus_code: str, authen: str) -> Dict[str, Any]:
        """Get all available semesters."""
        checksum = self.checksum.checksum_a(campus_code)
        
        url = f"{self.BASE_URL}/GetSemester"
        params = {
            'campusCode': campus_code,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def get_subject_by_semester(self, campus_code: str, semester: str, 
                               authen: str) -> Dict[str, Any]:
        """Get subjects for a specific semester."""
        checksum = self.checksum.checksum_k("", campus_code)
        
        url = f"{self.BASE_URL}/GetSubjectBySemester"
        params = {
            'campusCode': campus_code,
            'Semester': semester,
            'Authen': authen,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)
    
    def get_week_by_date(self, timestamp: str) -> Dict[str, Any]:
        """Get week number by date timestamp."""
        checksum = self.checksum.checksum_a(timestamp)
        
        url = f"{self.BASE_URL}/GetWeekByDate"
        params = {
            'date': timestamp,
        }
        
        return self._make_request('GET', url, params=params) 

    def get_student_attendances(self, campus_code: str, semester: str,
                                 roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student attendance summary for a semester."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        url = f"{self.BASE_URL}/GetStudentAttendances"
        params = {
            'campusCode': campus_code,
            'Semester': semester,
            'rollNumber': roll_number,
            'Authen': authen,
            'checksum': checksum
        }
        return self._make_request('GET', url, params=params)
    
    def get_exam_schedule(self, campus_code: str, semester: str,
                            roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student exam schedule for a semester."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        url = f"{self.BASE_URL}/GetScheduleExam"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Semester': semester,
            'Authen': authen,
            'checksum': checksum
        }
        return self._make_request('GET', url, params=params)
    
    def get_student_mark(self, campus_code: str, semester: str,
                          roll_number: str, authen: str) -> Dict[str, Any]:
        """Get student marks summary for a semester."""
        checksum = self.checksum.checksum_k(roll_number, campus_code)
        url = f"{self.BASE_URL}/GetStudentMark"
        params = {
            'campusCode': campus_code,
            'rollNumber': roll_number,
            'Semester': semester,
            'Authen': authen,
            'checksum': checksum
        }
        return self._make_request('GET', url, params=params)
    
    def get_top10_news(self, campus_code: str, authen: str, news_type: str) -> Dict[str, Any]:
        checksum = self.checksum.checksum_k(news_type, campus_code)
        
        url = f"{self.BASE_URL}/GetTop10News"
        params = {
            'campusCode': campus_code,
            'Authen': authen,
            'type': news_type,
            'checksum': checksum
        }
        
        return self._make_request('GET', url, params=params)