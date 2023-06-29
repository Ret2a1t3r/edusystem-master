#include<iostream>
#include<cstring>
#include<set>
#include<string>
#include<algorithm>
#include<fstream>
#include<vector>
#include<unordered_map>
#include<cstdio>
#include<cstdlib>

using namespace std;

unordered_map<string, int> lesson_map;
int lesson_cnt = 0;
vector<string> lesson_teacher[10000];

struct schedule //时间表
{
	bool class_time[20][8][11];//18周 一周七天一天10节课
	schedule() {
		for (int i = 0; i < 20; i++)
			for (int j = 0; j < 8; j++)
				for (int k = 0; k < 11; k++)
					this->class_time[i][j][k] = false;
	}
};

struct teacher//教师信息
{
	string name;//名字
	int birth_year;//出生年份
	string sex;//性别
	schedule time;//时间表
	int can_cnt;//老师能授课得总课数
	int cl;//老师要上得课的数量
	teacher():name(), birth_year(0), sex(), time(), can_cnt(0), cl(0) {}
	bool operator<(const teacher& t)const//按老师年龄排序
	{
		return birth_year < t.birth_year;
	}
};

struct class_room//教室信息
{
	int people_cnt;//教室容纳人数
	int class_number;//教室编号
	schedule time;//教室时间表
	class_room() :people_cnt(0), class_number(0), time() {}
	bool operator<(const class_room& t)const
	{
		return class_number < t.class_number;
	}
};

struct class_grade//班级信息
{
	int grade;//年级
	int major;//专业:1代表软件2代表计科3代表物联网
	int class_number;//班级号
	schedule time;//班级时间表
	string name;//班级名称如:20软件2班
	class_grade() : grade(0), major(0), class_number(0), time(), name() {}
};

struct date//存储上课时间
{
	int day;//星期几
	int start, end;//开始时间和结束时间
	int room_num;//上课房间
	date(): day(0), start(0), end(0), room_num(0){}
};

struct lesson
{
	int Grade;//上课年级
	string name;//课程名称
	string teacher_name;//老师名字
	vector<string> classes;//上课班级
	string classes_name;//上课班级名称为合并保证班级唯一给上课班级按照字典序排序
	int people_num;//上课人数
	bool have_theory;//是否为理论课
	bool have_exp;//是否为实验课
	int theory_number;//理论课节次
	int exp_number;//实验课节次
	vector<int> theory_week_start;//理论课开始周次
	vector<int> theory_week_end;//理论课结束周次
	vector<int> exp_week_start;//实验课开始周次
	vector<int> exp_week_end;//实验课结束周次
	vector<date> go_theory;//上理论课的时间地点
	vector<date> go_exp;//上实验课的时间
	vector<string> exp_teacher;//帮忙查实验的老师
	bool finish;//查看当前课程是否已排好

	lesson() :finish(false) {}

	bool operator<(lesson& t)const
	{
		if (name == t.name)
			return teacher_name < t.teacher_name;
		return name < t.name;
	}
};

bool read_class_grade(vector<class_grade>& grades, unordered_map<string, int>& grades_map)
{
	ifstream read("专业班级信息.csv");
	if (!read.is_open()) {
		cout << "未读到班级信息" << endl;
		return false;
	}
	string temp;
	getline(read, temp);
	while (getline(read, temp)) {
		int grade = 0, class_cnt = 0;//分别代表年级,班级数
		string temp_major = "";
		int i;
		for (i = 0; i < (int)temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			temp_major += temp[i];
		}

		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			grade = grade * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			class_cnt = class_cnt * 10 + temp[i] - '0';
		}

		for (int i = 1; i <= class_cnt; i++) {
			class_grade now;
			now.grade = grade;
			now.class_number = i;
			if (temp_major == "软工") now.major = 1;
			else if (temp_major == "计科") now.major = 2;
			else now.major = 3;
			for (int i = 1; i <= 7; i++)
				for (int j = 1; j <= 10; j++)
					for (int k = 1; k <= 18; k++)
						now.time.class_time[k][i][j] = false;
			for (int i = 1; i <= 18; i++) { //周三下午不能排课
				for (int j = 5; j <= 8; j++) {
					now.time.class_time[i][3][j] = true;
				}
			}
			string now_name = to_string(grade) + temp_major + to_string(i) + "班";
			now.name = now_name;
			grades.push_back(now);
			grades_map[now_name] = grades.size() - 1;
		}

	}
	read.close();
	return true;
}

bool read_teacher(vector<teacher>& teachers, unordered_map<string, int>& teachers_map)//读取老师信息
{
	ifstream read("老师信息.csv");
	if (!read.is_open()) {
		cout << "未读到教师信息" << endl;
		return false;
	}
	string temp;
	getline(read, temp);
	while (getline(read, temp)) {
		string name = "", sex = "";
		int age = 0;
		int i;
		for (i = 0; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			name += temp[i];
		}

		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			sex += temp[i];
		}

		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			age = age * 10 + temp[i] - '0';
		}
		teacher now;
		now.birth_year = age;
		now.name = name;
		now.sex = sex;
		for (int i = 1; i <= 7; i++)
			for (int j = 1; j <= 10; j++)
				for (int k = 1; k <= 18; k++)
					now.time.class_time[k][i][j] = false;
		now.can_cnt = 7 * 10 * 18;
		now.cl = 0;
		teachers.push_back(now);
		teachers_map[name] = teachers.size() - 1;
	}
	read.close();
	read.open("教师时间表.csv");
	if (!read.is_open()) {
		cout << "未找到教师时间表!" << endl;
		return false;
	}
	getline(read, temp);
	while (getline(read, temp)) {
		string name = "";//老师名字
		int week_start = 0, week_end = 0;//开始星期，结束星期
		int section_start = 0, section_end = 0;//开始节次，结束节次
		int i;
		for (i = 0; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			name += temp[i];
		}
		if (!teachers_map.count(name)) {
			cout << "教师信息文件中不存在:" + name << endl;
			return false;
		}
		int week_st = 0, week_ed = 0;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			if (temp[i] == '~') break;
			week_st = week_st * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			if (temp[i] == '~') break;
			week_ed = week_ed * 10 + temp[i] - '0';
		}
		for (int k = 1; k <= 4; k++) {
			for (i++; i < temp.size(); i++) {
				if (temp[i] == ',')
					break;
				if (temp[i] == ' ')
					continue;
				if (temp[i] == '~')
					break;
				if (k == 1) week_start = week_start * 10 + temp[i] - '0';
				else if (k == 2)week_end = week_end * 10 + temp[i] - '0';
				else if (k == 3) section_start = section_start * 10 + temp[i] - '0';
				else section_end = section_end * 10 + temp[i] - '0';
			}
		}
		int idx = teachers_map[name];
		for (int i = week_start; i <= week_end; i++)
			for (int j = section_start; j <= section_end; j++)
				for (int k = week_st; k <= week_ed; k++)
					if (!teachers[idx].time.class_time[k][i][j])
						teachers[idx].time.class_time[k][i][j] = true,
						teachers[idx].can_cnt--;
	}
	read.close();
	return true;
}

bool read_room(vector<class_room>& rooms, unordered_map<int, int>& rooms_map)
{
	ifstream read("教室信息.csv");
	if (!read.is_open()) {
		cout << "未读到教室信息" << endl;
		return false;
	}
	string temp;
	getline(read, temp);
	while (getline(read, temp)) {
		int room_num = 0, people_num = 0;
		int i;

		for (i = 0; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			room_num = room_num * 10 + temp[i] - '0';
		}

		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			people_num = people_num * 10 + temp[i] - '0';
		}

		class_room now;
		for (int i = 1; i <= 7; i++)
			for (int j = 1; j <= 10; j++)
				for (int k = 1; k <= 18; k++)
					now.time.class_time[k][i][j] = false;
		now.class_number = room_num;
		now.people_cnt = people_num;

		rooms.push_back(now);
	}
	read.close();
	sort(rooms.begin(),rooms.end());
	for (int i = 0; i < rooms.size(); i++) {
		rooms_map[rooms[i].class_number] = i;
	}
	return true;
}

bool read_class_file(ifstream& read, vector<lesson>& lessons,string file_name, 
	unordered_map<string, int>& grades_map,unordered_map<string, int>& teachers_map, vector<class_grade>& grades,
	vector<teacher> &teachers)
{
	string temp;
	int line = 1;
	getline(read,temp);
	while (getline(read, temp)) {
		line++;
		string name = "";//课程名称
		string teacher_name = "";//上课老师名字
		lesson now;
		int i;
		for (i = 0; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			name += temp[i];
		}
		now.name = name;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			teacher_name += temp[i];
		}
		if (!teachers_map.count(teacher_name)) {
			cout << file_name << "文件" <<"第"<<line<<"行" <<teacher_name <<
				"老师在老师文件中不存在" << endl;
			return false;
		}
		now.teacher_name = teacher_name;
		i++;
		while (temp[i] != ',') {
			if (temp[i] == '/')i++;
			string p = "";
			for (; i < temp.size(); i++) {
				if (temp[i] == ',') break;
				if (temp[i] == '/') break;
				if (temp[i] == ' ')continue;
				p += temp[i];
			}
			if (!grades_map.count(p)) {
				cout << file_name << "文件" << "第" << line << "行" << p <<
					"在专业年级文件中不存在" << endl;
				return false;
			}
			now.Grade = grades[grades_map[p]].grade;
			now.classes.push_back(p);
		}
		sort(now.classes.begin(), now.classes.end());
		now.classes_name = "";
		for (string s : now.classes)
			now.classes_name += s;
		int people = 0;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			people = people * 10 + temp[i] - '0';
		}
		now.people_num = people;
		i++;
		while (temp[i] != ',') {
			if (temp[i] == '/') i++;
			int start = 0, end = 0;
			for (; i < temp.size(); i++) {
				if (temp[i] == ',') break;
				if (temp[i] == '~') break;
				if (temp[i] == ' ') continue;
				start = start * 10 + temp[i] - '0';
			}
			if (start == 0) {
				now.have_theory = false;
				while (temp[i] != ',') i++;
				break;
			}else {
				now.have_theory = true;
				now.theory_week_start.push_back(start);
			}
			for (i++; i < temp.size(); i++) {
				if (temp[i] == ',') break;
				if (temp[i] == '/') break;
				if (temp[i] == ' ') continue;
				end = end * 10 + temp[i] - '0';
			}
			now.theory_week_end.push_back(end);
		}
		int theory = 0;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			theory = theory * 10 + temp[i] - '0';
		}
		now.theory_number = theory;
		if (theory) {
			for (size_t i = 0; i < now.theory_week_start.size(); i ++ )
				teachers[teachers_map[teacher_name]].cl += theory * (now.theory_week_end[i] - now.theory_week_start[i]);
		}
		i++;
		while (temp[i] != ',') {
			if (temp[i] == '/') i++;
			int start = 0, end = 0;
			for (; i < temp.size(); i++) {
				if (temp[i] == ',') break;
				if (temp[i] == '~') break;
				if (temp[i] == ' ') continue;
				start = start * 10 + temp[i] - '0';
			}
			if (start == 0) {
				now.have_exp = false;
				while (temp[i] != ',') i++;
				break;
			}
			else {
				if (!lesson_map.count(name)) {
					lesson_map[name] = ++lesson_cnt;
					lesson_teacher[lesson_cnt].push_back(teacher_name);
				}
				else {
					bool flag = true;
					for (string s : lesson_teacher[lesson_map[name]]) {
						if (s == teacher_name) {
							flag = false;
							break;
						}
					}
					if(flag)
						lesson_teacher[lesson_map[name]].push_back(teacher_name);
				}
				now.have_exp = true;
				now.exp_week_start.push_back(start);
			}
			for (i++; i < temp.size(); i++) {
				if (temp[i] == ',') break;
				if (temp[i] == '/') break;
				if (temp[i] == ' ') continue;
				end = end * 10 + temp[i] - '0';
			}
			now.exp_week_end.push_back(end);
		}
		int exp = 0;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			exp = exp * 10 + temp[i] - '0';
		}
		now.exp_number = exp;
		if (exp) {
			for (size_t i = 0; i < now.exp_week_start.size(); i ++ )
			teachers[teachers_map[teacher_name]].cl += exp * (now.exp_week_end[i] - now.exp_week_start[i]);
		}
		lessons.push_back(now);
	}
	return true;
}

bool write_class_file(vector<lesson>& lessons)
{
	ofstream computer_wirte("计算机.csv");
	if (computer_wirte.fail()) {
		cout << "写入计算机文件错误" << endl;
		return false;
	}
	ofstream software_wirte("软件.csv");
	if (software_wirte.fail()) {
		cout << "写入软件文件错误" << endl;
		return false;
	}
	computer_wirte << "学院,专业,年级,课程名称,教师姓名,上课班级,上课人数,上课地点,周次,星期,开始节次,结束节次,是否为实验课(0/1)" << endl;
	software_wirte << "学院,专业,年级,课程名称,教师姓名,上课班级,上课人数,上课地点,周次,星期,开始节次,结束节次,是否为实验课(0/1)" << endl;
	int num = 0;
	for (lesson now : lessons) {
		if (!now.finish) continue;
		string classes_temp = "";
		bool flag = false;//记录是不是第一个方便格式化
		for (string s : now.classes) {
			if (flag) classes_temp += "/" + s;
			else classes_temp += s;
			flag = true;
		}
		if(now.have_theory){
			string week_temp = "";
			flag = false;
			for (int i = 0; i < now.theory_week_start.size(); i++) {
				if (flag) week_temp += "/";
				week_temp += to_string(now.theory_week_start[i]) + "-" + to_string(now.theory_week_end[i])+"周";
				flag = true;
			}
			//cout <<num++<<" " << week_temp << endl;
			for (date dt : now.go_theory) {
				string ans = "20" + to_string(now.Grade) + ",";
				ans += now.name;
				ans += "," + now.teacher_name + "," + classes_temp + "," + to_string(now.people_num) + "," + "3号楼-"
					+ to_string(dt.room_num) + "," + week_temp + "," + to_string(dt.day) +
					"," + to_string(dt.start) + "," + to_string(dt.end) + ",0";
				if (classes_temp.find("软工") != string::npos) software_wirte <<"软件学院,软件工程,"+ ans << endl;
				else {
					if (classes_temp.find("计科") == string::npos) ans = "计算机学院,物联网," + ans;
					else ans = "计算机学院,计算机," + ans;
					computer_wirte << ans << endl;
				}
			}
		}
		if (now.have_exp) {
			string week_temp = "";
			flag = false;
			for (int i = 0; i < now.exp_week_start.size(); i++) {
				if (flag) week_temp += "/";
				week_temp += to_string(now.exp_week_start[i]) + "-" + to_string(now.exp_week_end[i])+"周";
				flag = true;
			}
			//cout << num++ << " " << week_temp << endl;
			for (date dt : now.go_exp) {
				string ans = "20" + to_string(now.Grade) + ",";
				ans += now.name;
				ans += "," + now.teacher_name + "," + classes_temp + "," + to_string(now.people_num) + "," + "4号楼-"
					+ "," + week_temp + "," + to_string(dt.day) +"," + to_string(dt.start) + "," + to_string(dt.end) + ",1";
				if (classes_temp.find("软工") != string::npos) software_wirte << "软件学院,软件工程," + ans << endl;
				else {
					if (classes_temp.find("计科") == string::npos) ans = "计算机学院,物联网," + ans;
					else ans = "计算机学院,计算机," + ans;
					computer_wirte << ans << endl;
				}
			}
		}
	}
	return true;
}

bool read_lessons(vector<lesson>& lessons, unordered_map<string, int>& grades_map, vector<teacher> &teachers,
					unordered_map<string, int>& teachers_map, vector<class_grade> &grades)
{
	ifstream read;
	bool read_success;
	read.open("软件必修.csv");
	if (!read.is_open()) {
		cout << "软件必修文件不存在" << endl;
		return false;
	}
	read_success = read_class_file(read,lessons,"软件必修", grades_map, teachers_map, grades,teachers);
	if (!read_success) {
		system("pause");
		exit(-1);
	}
	read.close();
	read.open("计算机必修.csv");
	if (!read.is_open()) {
		cout << "计算机必修文件不存在" << endl;
		return false;
	}
	read_success = read_class_file(read, lessons,"计算机必修", grades_map, teachers_map, grades,teachers);
	if (!read_success) {
		system("pause");
		exit(-1);
	}
	read.close();
	read.open("物联网必修.csv");
	if (!read.is_open()) {
		cout << "物联网必修文件不存在" << endl;
		return false;
	}
	read_success = read_class_file(read, lessons,"物联网必修", grades_map, teachers_map, grades,teachers);
	if (!read_success) {
		system("pause");
		exit(-1);
	}
	read.close();
	read.open("专业选修.csv");
	if (!read.is_open()) {
		cout << "专业选修文件不存在" << endl;
		return false;
	}
	read_success = read_class_file(read, lessons,"专业选修", grades_map, teachers_map, grades,teachers);
	if (!read_success) {
		system("pause");
		exit(-1);
	}
	read.close();
	return true;
}

bool read_other_class(vector<class_grade>& grades, unordered_map<string, int>& grades_map)//读取其他院拍好的课
{
	ifstream read;
	read.open("其他院排好的课.csv");
	if (!read.is_open()) {
		cout << "没有其他院开好的课的文件" << endl;
		return false;
	}
	string temp;
	getline(read,temp);
	while (getline(read, temp)) {
		int i = 0;
		vector<string> grade_name;//当前课程上课班级
		vector<int> week_start, week_end;//开始周次与结束周次
		int class_start = 0, class_end = 0;//开始节次与结束节次
		int week = 0;//上课是星期几
		while (temp[i] != ',') i++; // 课程名称没用跳过
		i++;
		while (temp[i] != ',') {
			string now_grade = "";
			if (temp[i] == '/') i++;
			for (; i < temp.size(); i++) {
				if (temp[i] == ',')
					break;
				if (temp[i] == '/')
					break;
				if (temp[i] == ' ')
					continue;
				now_grade += temp[i];
			}
			grade_name.push_back(now_grade);
		}
		i++;
		while (temp[i] != ',') {
			int start = 0, end = 0;
			if (temp[i] == '/') i++;
			for (; i < temp.size(); i++) {
				if (temp[i] == ',')
					break;
				if (temp[i] == '~')
					break;
				if (temp[i] == ' ')
					continue;
				start = start * 10 + temp[i] - '0';
			}
			week_start.push_back(start);
			for (i++; i < temp.size(); i++) {
				if (temp[i] == ',' || temp[i] == '/')
					break;
				if (temp[i] == ' ')
					continue;
				if (temp[i] >= '0' && temp[i] <= '9')
					end = end * 10 + temp[i] - '0';
			}
			week_end.push_back(end);
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			week = week * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			class_start = class_start * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',')
				break;
			if (temp[i] == ' ')
				continue;
			class_end = class_end * 10 + temp[i] - '0';
		}
		for (int i = 0; i < week_start.size(); i++) {
			int start = week_start[i], end = week_end[i];
			for (int j = start; j <= end; j++) {
				for (int k = class_start; k <= class_end; k++) {
					for (string s : grade_name) {
						int p = grades_map[s];
						grades[p].time.class_time[j][week][k] = true;
					}
				}
			}
		}
	}
	return true;
}

bool read_success_lesson(vector<class_grade> &grades, unordered_map<string, int> &grades_map,
						vector<teacher> &teachers, unordered_map<string, int> &teachers_map,
						vector<class_room> &rooms, unordered_map<int, int> &rooms_map) {//读取成功排好课的文件
	ifstream read;
	read.open("排好的课的文件.csv");
	if (!read.is_open()) {
		return false;
	}
	string temp;
	getline(read,temp);
	while (getline(read, temp)) {
		int cnt = 0;//记录逗号个数 
		int i = 0;
		while (cnt != 4) {
			while (temp[i] != ',') i++;
			i++;
			cnt++;
		}
		string teacher_name("");
		for (; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			teacher_name += temp[i];
		}
		vector<string> grades_name;
		string grade_name_temp="";
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') {
				grades_name.push_back(grade_name_temp);
				break;
			}
			if (temp[i] == ' ') continue;
			if (temp[i] == '/') {
				grades_name.push_back(grade_name_temp);
				grade_name_temp = "";
				continue;
			}
			grade_name_temp += temp[i];
		}
		for (i++; temp[i] != ','; i++);
		string class_room = "";
		int room = 0;
		bool has_room = false;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			class_room += temp[i];
			if (has_room) room = room * 10 + temp[i] - '0';
			if (temp[i] == '-'&&(temp[i+1]>='0'&&temp[i+1]<='9')) has_room = true;
		}
		int st = 0, ed = 0, day = 0;
		vector<int> week_st, week_ed;
		i++;
		while (temp[i] != ',') {
			st = ed = 0;
			while (temp[i] != '-') {
				st = st * 10 + temp[i] - '0';
				i++;
			}
			i++;
			while (temp[i] >= '0' && temp[i] <= '9') {
				ed = ed * 10 + temp[i] - '0';
				i++;
			}
			week_st.push_back(st);
			week_ed.push_back(ed);
			while (temp[i] != ',' && temp[i] != '/') i++;
			if (temp[i] == ',') break;
			i++;
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			day = day * 10 + temp[i] - '0';
		}
		int class_st = 0, class_ed = 0;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			class_st = class_st * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			class_ed = class_ed * 10 + temp[i] - '0';
		}
		int teacher_num = teachers_map[teacher_name];
		for (size_t p = 0; p < week_st.size(); p++) {
			int ws = week_st[p], wd = week_ed[p];
			for (int i = ws; i <= wd; i++) {
				for (int j = class_st; j <= class_ed; j++) {
					teachers[teacher_num].time.class_time[i][day][j] = true;
					if (has_room) rooms[rooms_map[room]].time.class_time[i][day][j] = true;
					for (string now : grades_name) {
						int grades_num = grades_map[now];
						grades[grades_num].time.class_time[i][day][j] = true;
					}
				}
			}
		}
	}
}

bool read_teacher_time(vector<pair<int, string>> &teacher_time, vector<teacher>& teachers, 
						unordered_map<string, int>& teachers_map){
	unordered_map<string, int> teacher_time_map;
	ifstream read;
	read.open("教师需求上课时间表.csv");
	if (!read.is_open()) {
		return false;
	}
	string temp;
	getline(read,temp);
	while (getline(read, temp)) {
		string teacher_name = "";
		int i = 0, week_st = 0, week_ed = 0, day_st = 0, day_ed = 0, class_st = 0, class_ed = 0;
		for (; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			teacher_name += temp[i];
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == '~') break;
			if (temp[i] == ' ') continue;
			week_st = week_st * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			week_ed = week_ed * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == '~') break;
			if (temp[i] == ' ') continue;
			day_st = day_st * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			day_ed = day_ed * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			class_st = class_st * 10 + temp[i] - '0';
		}
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == ' ') continue;
			class_ed = class_ed * 10 + temp[i] - '0';
		}
		if (!teacher_time_map.count(teacher_name)) {
			teacher_time_map[teacher_name] = teacher_time.size();
			teacher_time.push_back({0,teacher_name});
			int teacher_num = teachers_map[teacher_name];
			for (int i = 1; i <= 18; i++)
				for (int j = 1; j <= 7; j++)
					for (int k = 1; k <= 10; k++)
						teachers[teacher_num].time.class_time[i][j][k] = true;
		}
		int time_num = teacher_time_map[teacher_name], teacher_num = teachers_map[teacher_name];
		teachers[teacher_num].can_cnt = 0;
		for (int i = week_st; i <= week_ed; i++)
			for (int j = day_st; j <= day_ed; j++)
				for (int k = class_st; k <= class_ed; k++)
					teachers[teacher_num].time.class_time[i][j][k] = false,
					teachers[teacher_num].can_cnt++,
					teacher_time[time_num].first++;
	}

}

struct class_table//写到课表文件中用的结构体
{
	string s;
	int grade,week_ed,day,st;//年纪,课程结束周次,星期,开始节次
	vector<string> major;//专业
	bool operator<(const class_table &obj)const {
		if (day == obj.day && st == obj.st) return week_ed < obj.week_ed;
		if (day == obj.day) return st < obj.st;
		return day < obj.day;
	}
};

void read_lessons_file(ifstream &read,vector<class_table> &lessons)
{
	string temp;
	getline(read,temp);
	while (getline(read, temp)) {
		class_table now;
		now.s = temp;
		int i = 0,cnt = 0;
		while (cnt != 2) {
			cnt++;
			while (temp[i] != ',') i++;
			i++;
		}
		now.grade = 0;
		for (; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			now.grade = now.grade * 10 + temp[i] - '0';
		}
		i++;
		cnt = 0;
		while (cnt != 2) {
			cnt++;
			while (temp[i] != ',') i++;
			i++;
		}
		string p = "";
		for (; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			p += temp[i];
		}
		if (p.find("软工") != string::npos) now.major.push_back("软件工程");
		if (p.find("计科") != string::npos) now.major.push_back("计算机");
		if (p.find("物联网") != string::npos) now.major.push_back("物联网");
		cnt = 0;
		i++;
		while (cnt != 2) {
			cnt++;
			while (temp[i] != ',') i++;
			i++;
		}
		while (temp[i] != '-') i++;
		now.week_ed = 0;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			if (temp[i] == '/') {
				while (temp[i] != ',') i++;
				now.week_ed = 18;
				break;
			}
			if(temp[i]>='0'&&temp[i]<='9') now.week_ed = now.week_ed * 10 + temp[i] - '0';
		}
		now.day = 0;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			now.day = now.day * 10 + temp[i] - '0';
		}
		now.st = 0;
		for (i++; i < temp.size(); i++) {
			if (temp[i] == ',') break;
			now.st = now.st * 10 + temp[i] - '0';
		}
		lessons.push_back(now);
	}
}

bool create_class_table()//生成课表
{
	ifstream read;
	vector<class_table> lessons;
	read.open("软件.csv");
	if (!read.is_open()) {
		cout << "打开软件.csv文件失败" << endl;
		return false;
	}
	read_lessons_file(read,lessons);
	read.close();
	read.open("计算机.csv");
	if (!read.is_open()) {
		cout << "打开计算机.csv文件失败" << endl;
		return false;
	}
	read_lessons_file(read, lessons);
	read.close();
	vector<ofstream*> write;
	unordered_map<string, int> write_map;
	ofstream* write_temp = nullptr;
	sort(lessons.begin(),lessons.end());
	for (size_t i = 0; i < lessons.size(); i++) {
		for (size_t j = 0; j < lessons[i].major.size(); j++){
			if (!write_map.count(to_string(lessons[i].grade) + lessons[i].major[j])) {
				write_temp = new ofstream(to_string(lessons[i].grade) + lessons[i].major[j] + ".csv");
				if (!write_temp->is_open()) {
					cout << "打开" << to_string(lessons[i].grade) + lessons[i].major[j] << "文件失败" << endl;
					return false;
				}
				*write_temp << 
				"学院,专业,年级,课程名称,教师姓名,上课班级,上课人数,上课地点,周次,星期,开始节次,结束节次,是否为实验课(0/1)" << endl;
				write_map[to_string(lessons[i].grade) + lessons[i].major[j]] = write.size();
				write.push_back(write_temp);
			}
			*write[write_map[to_string(lessons[i].grade) + lessons[i].major[j]]] << lessons[i].s << endl;
		}
	}
	for (size_t i = 0; i < write.size(); i++) {
		write[i]->close();
		delete write[i];
	}
	return true;
}

vector<class_grade> grades;//存储班级信息
unordered_map<string, int> grades_map;//存储对应班级对应序号
vector<teacher> teachers;//存储老师信息
unordered_map<string, int> teachers_map;//存储对应老师对应序号
vector<class_room> rooms;//存储教室信息
unordered_map<int, int> rooms_map;//存储对应教室对应序号
vector<lesson> lessons;//存储要上的课
vector<pair<int, string>> teacher_time;
int room_block;

bool read_exp_teacher()//读取帮忙查实验的老师
{
	ifstream read;
	read.open("带实验.csv");
	if (!read.is_open()) {
		cout << "没有带实验文件" << endl;
		return false;
	}
	string temp;
	int line = 1;
	getline(read, temp);
	while (getline(read, temp))
	{
		line++;
		vector<string> classes;
		int i = 0;
		while (temp[i] != ',')
		{
			string s = "";
			while (temp[i] != ',' && temp[i] != '/')
			{
				s += temp[i];
				i++;
			}
			if (temp[i] == '/') i++;
			if (!grades_map.count(s))
			{
				cout << "带实验文件第" << line << "行" << s << "不存在" << endl;
				return false;
			}
			classes.push_back(s);
		}
		string lesson_name = "";
		i++;
		while (temp[i] != ',')
		{
			lesson_name += temp[i];
			i++;
		}
		string teacher_name = "";
		i++;
		while (temp[i] != ',')
		{
			teacher_name += temp[i];
			i++;
		}
		if (!teachers_map.count(teacher_name))
		{
			cout << "带实验文件第" << line << "行" << teacher_name << "不存在" << endl;
			return false;
		}
		string s = "";
		vector<string> exp_teacher;
		for (i++; i < temp.size(); i++)
		{
			if (temp[i] == ' ') continue;
			if (temp[i] == ',')
			{
				if (s == "") continue;
				exp_teacher.push_back(s);
				if (!teachers_map.count(s))
				{
					cout << "带实验文件第" << line << "行" << s << "不存在" << endl;
					return false;
				}
				s = "";
				continue;
			}
			s += temp[i];
		}
		if (s != "")
		{
			if (!teachers_map.count(s))
			{
				cout << "带实验文件第" << line << "行" << s << "不存在" << endl;
				return false;
			}
			exp_teacher.push_back(s);
		}
		sort(classes.begin(), classes.end());
		string classes_name = "";
		for (string s : classes) classes_name += s;
		bool success = false;
		for (lesson &ls : lessons)
		{
			if (ls.name == lesson_name && ls.classes_name == classes_name
				&& ls.teacher_name == teacher_name)
			{
				success = true;
				ls.exp_teacher = exp_teacher;
				break;
			}
		}
		if (!success)
		{
			cout << "带实验文件第" << line << "行课程信息不存在" << endl;
			return false;
		}
	}
	read.close();
	return true;
}

bool include(string s1, string s2)//求两个字符串是否为包含关系
{
	if (s1.size() > s2.size()) swap(s1, s2);
	for (size_t i = 0; i < s2.size(); i++)
	{
		bool flag = true;
		for (size_t j = 0; j < s1.size(); j++)
		{
			if (i + j >= s2.size() || s2[i + j] != s1[j])
			{
				flag = false;
				break;
			}
		}
		if (flag) return true;
	}
	return false;
}

bool sort_same_time_lesson()
{
	ifstream read;
	read.open("同时间片课程.csv");
	if (!read.is_open()){
		cout << "打开同时间片课程文件失败" << endl;
		return false;
	}
	string temp;
	int line = 1;
	getline(read, temp);
	while (getline(read, temp))
	{
		vector<string> classes;
		int i = 0;
		string s = "";
		line++;
		while (true)
		{
			if (temp[i] == ' ')
			{
				i++;
				continue;
			}
			if (temp[i] == ',')
			{
				classes.push_back(s);
				break;
			}
			if (temp[i] == '/')
			{
				classes.push_back(s);
				i++;
				s = "";
			}
			s += temp[i];
			i++;
		}
		i++;
		sort(classes.begin(), classes.end());
		string classes_name = "";
		for (string s : classes) classes_name += s;
		vector<string> lesson_names, teacher_names;
		string ln = "", tn = "";
		while (i < temp.size())
		{
			while (i < temp.size() && temp[i] != ',')
			{
				if (temp[i] == ' ')
				{
					i++;
					continue;
				}
				ln += temp[i];
				i++;
			}
			i++;
			while (i < temp.size() && temp[i] != ',')
			{
				if (temp[i] == ' ')
				{
					i++;
					continue;
				}
				tn += temp[i];
				i++;
			}
			i++;
			if (ln != "" && tn != "")
			{
				lesson_names.push_back(ln);
				teacher_names.push_back(tn);
				ln = tn = "";
			}
		}
		vector<int> lesson_nums;
		int the_num = 0, exp_num = 0;
		for (int i = 0; i < lesson_names.size(); i++)
		{
			ln = lesson_names[i], tn = teacher_names[i];
			bool flag = false;// 看看有没有找到
			for (int j = 0; j < lessons.size(); j++)
			{
				if (include(lessons[j].classes_name, classes_name) && lessons[j].name == ln
					&& lessons[j].teacher_name == tn)
				{
					lessons[j].finish = true;
					lesson_nums.push_back(j);
					flag = true;
					the_num = max(the_num, lessons[j].theory_number);
					exp_num = max(exp_num, lessons[j].exp_number);
					break;
				}
			}
			if (!flag) {
				cout << "同时间片课程文件中第" << line << "行" << ln << "不存在" << endl;
				return false;
			}
		}
		int now_room_block = 0;
		for (int week = 1; week <= 18; week++)
		{
			int cnt = 0;
			for (int lnum : lesson_nums)
			{
				if (!lessons[lnum].have_theory) continue;
				for (size_t i = 0; i < lessons[lnum].theory_week_start.size(); i++)
				{
					if (lessons[lnum].theory_week_start[i] <= week &&
						lessons[lnum].theory_week_end[i] >= week)
					{
						cnt++;
						break;
					}
				}
			}
			now_room_block = max(now_room_block, cnt);
		}
		int day = 1;//从周一开始
		int last_the_num = 0, room_start = 0;
		while (the_num) // 排理论课
		{
			if (last_the_num == the_num) room_start++;
			last_the_num = the_num;
			for (int cl_st = 1; cl_st <= 9; cl_st += 2)
			{
				bool room_can = true, teacher_can = true, stu_can = true;
				for (int ls_num : lesson_nums)
				{
					if (!lessons[ls_num].theory_number) continue;
					for (size_t p = 0; p < lessons[ls_num].theory_week_start.size(); p++)
					{
						int week_st = lessons[ls_num].theory_week_start[p];
						int week_ed = lessons[ls_num].theory_week_end[p];
						for (int week = week_st; week <= week_ed; week++)
						{
							if (teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st] ||
								teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st + 1])
							{
								teacher_can = false;
								break;
							}
							for (string cl_name : lessons[ls_num].classes)
							{
								if (grades[grades_map[cl_name]].time.class_time[week][day][cl_st] ||
									grades[grades_map[cl_name]].time.class_time[week][day][cl_st + 1])
								{
									stu_can = false;
									break;
								}
							}
							if (!stu_can) break;
							for (int rm_num = room_start; rm_num < room_start + now_room_block; rm_num++)
							{
								if (rooms[rm_num].time.class_time[week][day][cl_st] ||
									rooms[rm_num].time.class_time[week][day][cl_st + 1])
								{
									room_can = false;
									break;
								}
							}
							if (!room_can) break;
						}
						if ((!room_can) || (!stu_can) || (!teacher_can)) break;
					}
					if ((!room_can) || (!stu_can) || (!teacher_can)) break;
				}
				if ((!room_can) || (!stu_can) || (!teacher_can)) continue;
				the_num -= 2;
				for (int ls_num : lesson_nums)
				{
					if (!lessons[ls_num].theory_number) continue;
					for (int rm_num = room_start; rm_num < room_start + now_room_block; rm_num++)
					{
						bool rm_can = true;
						for (size_t p = 0; p < lessons[ls_num].theory_week_start.size(); p++)
						{
							int week_st = lessons[ls_num].theory_week_start[p];
							int week_ed = lessons[ls_num].theory_week_end[p];
							for (int week = week_st; week <= week_ed; week++)
							{
								if (rooms[rm_num].time.class_time[week][day][cl_st] ||
									rooms[rm_num].time.class_time[week][day][cl_st + 1])
								{
									rm_can = false;
									break;
								}
							}
							if (!rm_can) break;
						}
						if (!rm_can) continue;
						lessons[ls_num].theory_number -= 2;
						for (size_t p = 0; p < lessons[ls_num].theory_week_start.size(); p++)
						{
							int week_st = lessons[ls_num].theory_week_start[p];
							int week_ed = lessons[ls_num].theory_week_end[p];
							for (int week = week_st; week <= week_ed; week++)
							{
								teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st] = true;
								teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st + 1] = true;
								for (string cl_name : lessons[ls_num].classes)
								{
									grades[grades_map[cl_name]].time.class_time[week][day][cl_st] = true;
									grades[grades_map[cl_name]].time.class_time[week][day][cl_st + 1] = true;
								}
								rooms[rm_num].time.class_time[week][day][cl_st] = true;
								rooms[rm_num].time.class_time[week][day][cl_st + 1] = true;
							}
						}
						date now;
						now.start = cl_st;
						now.end = cl_st + 1;
						now.room_num = rooms[rm_num].class_number;
						now.day = day;
						lessons[ls_num].go_theory.push_back(now);
						break;
					}
				}
				break;
			}
			if (last_the_num == the_num) day++;
			else day += 2;
			if (day > 7) day = day % 7;
		}
		int last_exp_num = 0;
		while (exp_num) // 排实验课
		{
			last_exp_num = exp_num;
			for (int cl_st = 1; cl_st <= 9; cl_st += 2)
			{
				bool teacher_can = true, stu_can = true, other_teacher_can = true;
				for (int ls_num : lesson_nums)
				{
					if (!lessons[ls_num].exp_number) continue;
					for (size_t p = 0; p < lessons[ls_num].exp_week_start.size(); p++)
					{
						int week_st = lessons[ls_num].exp_week_start[p];
						int week_ed = lessons[ls_num].exp_week_end[p];
						for (int week = week_st; week <= week_ed; week++)
						{
							if (teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st] ||
								teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st + 1])
							{
								teacher_can = false;
								break;
							}
							for (string cl_name : lessons[ls_num].classes)
							{
								if (grades[grades_map[cl_name]].time.class_time[week][day][cl_st] ||
									grades[grades_map[cl_name]].time.class_time[week][day][cl_st + 1])
								{
									stu_can = false;
									break;
								}
							}
							if (!stu_can) break;
							for (string other_teacher : lessons[ls_num].exp_teacher)
							{
								if (teachers[teachers_map[other_teacher]].time.class_time[week][day][cl_st] ||
									teachers[teachers_map[other_teacher]].time.class_time[week][day][cl_st + 1])
								{
									other_teacher_can = false;
									break;
								}
							}
							if (!other_teacher_can) break;
						}
						if ((!stu_can) || (!teacher_can) || (!other_teacher_can)) break;
					}
					if ((!stu_can) || (!teacher_can) || (!other_teacher_can)) break;
				}
				if ((!stu_can) || (!teacher_can) || (!other_teacher_can)) continue;
				exp_num -= 2;
				for (int ls_num : lesson_nums)
				{
					if (!lessons[ls_num].exp_number) continue;
					lessons[ls_num].exp_number -= 2;
					for (size_t p = 0; p < lessons[ls_num].exp_week_start.size(); p++)
					{
						int week_st = lessons[ls_num].exp_week_start[p];
						int week_ed = lessons[ls_num].exp_week_end[p];
						for (int week = week_st; week <= week_ed; week++)
						{
							teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st] = true;
							teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st + 1] = true;
							for (string cl_name : lessons[ls_num].classes)
							{
								grades[grades_map[cl_name]].time.class_time[week][day][cl_st] = true;
								grades[grades_map[cl_name]].time.class_time[week][day][cl_st + 1] = true;
							}
							for (string other_teacher : lessons[ls_num].exp_teacher)
							{
								teachers[teachers_map[other_teacher]].time.class_time[week][day][cl_st] = true;
								teachers[teachers_map[other_teacher]].time.class_time[week][day][cl_st + 1] = true;
							}
						}
					}
					date now;
					now.day = day;
					now.start = cl_st;
					now.end = cl_st + 1;
					lessons[ls_num].go_exp.push_back(now);
				}
				break;
			}
			if (last_exp_num == exp_num) day++;
			else day += 2;
			if (day > 7) day = day % 7;
		}
	}
	return true;
}

bool normal_sort()
{
	sort(lessons.begin(), lessons.end(), [&](lesson a, lesson b)->bool {
		int a_idx = teachers_map[a.teacher_name], b_idx = teachers_map[b.teacher_name];
		double a_ave = (double)teachers[a_idx].cl / teachers[a_idx].can_cnt, b_ave = (double)teachers[b_idx].cl / teachers[b_idx].can_cnt;
		if (a.exp_teacher.size() != b.exp_teacher.size()) return a.exp_teacher.size() > b.exp_teacher.size();
		if (teachers[a_idx].can_cnt == teachers[b_idx].can_cnt && fabs(a_ave - b_ave) < 1e-6)
			return teachers[a_idx].birth_year < teachers[b_idx].birth_year;
		if (fabs(a_ave - b_ave) < 1e-6) return teachers[a_idx].can_cnt < teachers[b_idx].can_cnt;
		return a_ave > b_ave;
		});
	for (size_t i = 0; i < lessons.size(); i++)
	{
		if (lessons[i].teacher_name == "王嘉芳") continue;
		for (size_t j = i + 1; j < lessons.size(); j++)
		{
			if (lessons[j].teacher_name == "王嘉芳" && lessons[i].teacher_name != "王嘉芳")
			{
				swap(lessons[i], lessons[j]);
				break;
			}
		}
	}
	for (int ls_num = 0; ls_num < lessons.size(); ls_num++) {
		printf("%.2lf%%\n", (double)ls_num / lessons.size() * 100);
		if (lessons[ls_num].finish) continue;
		int the_num = lessons[ls_num].theory_number, exp_num = lessons[ls_num].exp_number;
		int last_the_num = 0, room_start = 0;
		int day = 1;
		bool days[10] = { 0 };
		while (the_num)
		{
			bool day_flag = true;
			for (int i = 1; i <= 7; i++)
			{
				if (!days[i])
				{
					day_flag = false;
					break;
				}
			}
			days[day] = true;
			if (last_the_num == the_num && day_flag) room_start++;
			last_the_num = the_num;
			if (room_start * room_block >= rooms.size())
			{
				cout << "排" << lessons[ls_num].name << lessons[ls_num].teacher_name << "失败";
				return false;
			}
			for (int cl_st = 1; cl_st <= 9; cl_st += 2)
			{
				bool teacher_can = true, stu_can = true;
				for (int rm_num = room_start * room_block; rm_num < room_start * room_block + room_block; rm_num++)
				{
					bool room_can = true;
					for (size_t p = 0; p < lessons[ls_num].theory_week_start.size(); p++)
					{
						int week_st = lessons[ls_num].theory_week_start[p];
						int week_ed = lessons[ls_num].theory_week_end[p];
						for (int week = week_st; week <= week_ed; week++)
						{
							if (teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st] ||
								teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st + 1])
							{
								teacher_can = false;
								break;
							}
							for (string cl_name : lessons[ls_num].classes)
							{
								if (grades[grades_map[cl_name]].time.class_time[week][day][cl_st] ||
									grades[grades_map[cl_name]].time.class_time[week][day][cl_st + 1])
								{
									stu_can = false;
									break;
								}
							}
							if (!stu_can) break;
							if (rooms[rm_num].time.class_time[week][day][cl_st] ||
								rooms[rm_num].time.class_time[week][day][cl_st + 1])
							{
								room_can = false;
								break;
							}
						}
						if ((!room_can) || (!stu_can) || (!teacher_can)) break;
					}
					if ((!teacher_can) || (!stu_can)) break;
					if (!room_can) continue;
					the_num -= 2;
					for (size_t p = 0; p < lessons[ls_num].theory_week_start.size(); p++)
					{
						int week_st = lessons[ls_num].theory_week_start[p];
						int week_ed = lessons[ls_num].theory_week_end[p];
						for (int week = week_st; week <= week_ed; week++)
						{
							teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st] = true;
							teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st + 1] = true;
							for (string cl_name : lessons[ls_num].classes)
							{
								grades[grades_map[cl_name]].time.class_time[week][day][cl_st] = true;
								grades[grades_map[cl_name]].time.class_time[week][day][cl_st + 1] = true;
							}
							rooms[rm_num].time.class_time[week][day][cl_st] = true;
							rooms[rm_num].time.class_time[week][day][cl_st + 1] = true;
						}
					}
					date now;
					now.start = cl_st;
					now.end = cl_st + 1;
					now.room_num = rooms[rm_num].class_number;
					now.day = day;
					lessons[ls_num].go_theory.push_back(now);
					break;
				}
				if (the_num != last_the_num) break;
			}
			if (last_the_num == the_num) day++;
			else day += 2;
			if (day > 7) day = day % 7;
		}
		int last_exp_num = 0;
		while (exp_num)
		{
			last_exp_num = exp_num;
			for (int cl_st = 1; cl_st <= 9; cl_st += 2)
			{
				bool teacher_can = true, stu_can = true, other_teacher_can = true;
				for (size_t p = 0; p < lessons[ls_num].theory_week_start.size(); p++)
				{
					int week_st = lessons[ls_num].theory_week_start[p];
					int week_ed = lessons[ls_num].theory_week_end[p];
					for (int week = week_st; week <= week_ed; week++)
					{
						if (teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st] ||
							teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st + 1])
						{
							teacher_can = false;
							break;
						}
						for (string cl_name : lessons[ls_num].classes)
						{
							if (grades[grades_map[cl_name]].time.class_time[week][day][cl_st] ||
								grades[grades_map[cl_name]].time.class_time[week][day][cl_st + 1])
							{
								stu_can = false;
								break;
							}
						}
						if (!stu_can) break;
						for (string exp_teacher_name : lessons[ls_num].exp_teacher)
						{
							if (teachers[teachers_map[exp_teacher_name]].time.class_time[week][day][cl_st] ||
								teachers[teachers_map[exp_teacher_name]].time.class_time[week][day][cl_st + 1])
							{
								other_teacher_can = false;
								break;
							}
						}
						if (!other_teacher_can) break;
					}
					if ((!stu_can) || (!teacher_can) || (!other_teacher_can)) break;
				}
				if ((!stu_can) || (!teacher_can) || (!other_teacher_can)) continue;
				exp_num -= 2;
				for (size_t p = 0; p < lessons[ls_num].theory_week_start.size(); p++)
				{
					int week_st = lessons[ls_num].exp_week_start[p];
					int week_ed = lessons[ls_num].exp_week_end[p];
					for (int week = week_st; week <= week_ed; week++)
					{
						teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st] = true;
						teachers[teachers_map[lessons[ls_num].teacher_name]].time.class_time[week][day][cl_st + 1] = true;
						for (string cl_name : lessons[ls_num].classes)
						{
							grades[grades_map[cl_name]].time.class_time[week][day][cl_st] = true;
							grades[grades_map[cl_name]].time.class_time[week][day][cl_st + 1] = true;
						}
						for (string other_teacher : lessons[ls_num].exp_teacher)
						{
							teachers[teachers_map[other_teacher]].time.class_time[week][day][cl_st] = true;
							teachers[teachers_map[other_teacher]].time.class_time[week][day][cl_st + 1] = true;
						}
					}
				}
				date now;
				now.day = day;
				now.start = cl_st;
				now.end = cl_st + 1;
				lessons[ls_num].go_exp.push_back(now);
				break;
			}
			if (last_the_num == the_num) day++;
			else day += 2;
			if (day > 7) day = day % 7;
		}
		lessons[ls_num].finish = true;
	}
	return true;
}

void sort_lesson()//排课
{
	if (!read_exp_teacher()) exit(-1);
	if (rooms.size() % 3 == 0) room_block = 3;
	else room_block = 2;
	if (!sort_same_time_lesson()) exit(-1);
	if (!normal_sort()) exit(-1);
}

int main()
{

	bool read_succse;

	read_succse = read_class_grade(grades, grades_map);
	if (read_succse == false) {
		system("pause");
		exit(-1);
	}

	read_succse = read_teacher(teachers, teachers_map);
	if (read_succse == false) {
		system("pause");
		exit(-1);
	}

	read_succse = read_room(rooms, rooms_map);
	if (read_succse == false) {
		system("pause");
		exit(-1);
	}

	read_succse = read_other_class(grades, grades_map);
	if (read_succse == false) {
		system("pause");
		exit(-1);
	}
	
	read_succse = read_lessons(lessons, grades_map,teachers, teachers_map,grades);

	read_success_lesson(grades,grades_map,teachers,teachers_map,rooms,rooms_map);

	read_teacher_time(teacher_time,teachers,teachers_map);
	
	sort_lesson();

	write_class_file(lessons);
	
	cout << "排课成功" << endl;
	create_class_table();
	system("pause");
	return 0;
}