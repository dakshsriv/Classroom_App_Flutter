import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter_conditional_rendering/flutter_conditional_rendering.dart';
import 'package:dio/dio.dart';

void main() async {
  await GetStorage.init();
  runApp(const Report());
}

final box = GetStorage();

class Report extends StatefulWidget {
  const Report({super.key});

  @override
  State<Report> createState() => _ReportState();
}

class _ReportState extends State<Report> {
  String userID = "";
  String accountType = "";
  String classID = "";
  dynamic report = [];
  List<dynamic> students = [];
  List<dynamic> assignments = [];
  

  void setup() async {
    try {
      DioClient x = DioClient();
      var reportc = await x.report();
      classID = await box.read("userID");
      setState(() {
        report = reportc[0];
        students = reportc[1];
        assignments = reportc[2];
        print(students[0].runtimeType);
      });
    } catch (e) {
      print("Fail");
      SchedulerBinding.instance.addPostFrameCallback((_) {
        Navigator.pushNamedAndRemoveUntil(context, "/", (_) => false);
      });
    }
  }

  @override
  void initState() {
    super.initState();

    setup();

    /*SchedulerBinding.instance.addPostFrameCallback((_) {
      userID = box.read("userID");
      accountType = box.read("accountType");
      if (userID == null)
      {
        Navigator.of(context).pushNamed("/login/");
      }
      
    });*/
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
            backgroundColor: Colors.blue, title: const Text("Classroom App")),
        body: Column(children: [
          Column(children: [
            TextButton(
              onPressed: () {
                Navigator.pushNamedAndRemoveUntil(
                    context, "/classroom/", (_) => false);
              },
              child: const Text('Back to class'),
            ),
            Text("Class ID: $classID"),
            const Text("Report:"),
            Container(
              margin: EdgeInsets.all(20),
              child: Table(
                defaultColumnWidth: FixedColumnWidth(120.0),
                border: TableBorder.all(
                    color: Colors.black, style: BorderStyle.solid, width: 2),
                children: [
                  TableRow( children: [  
                        Column(children:[Text('        ')]),  
                        for (var assignmenta in assignments)
                          Column(children:[Text('$assignmenta')]),
                          
                      ]), 
                  for (var student in students)
                    TableRow( children: [  
                        Column(children:[Text('$student')]),
                        for (var assignment in assignments)  
                          Conditional.single(
                            context: context,
                            conditionBuilder: (BuildContext context) => report[student][assignment][0][0] == 1,
                            widgetBuilder: (BuildContext context) => Column(children:[Text('Submitted')]),  
                            fallbackBuilder: (BuildContext context) => Column(children:[Text('Not submitted')]),
                          ),
                           
                      ]), 
                ]
                      
                    
                ,
              ),
            ),
          ])
        ]));
  }
}

class DioClient {
  final Dio _dio = Dio();
  final box = GetStorage();
  final _baseUrl = 'https://dev.dakshsrivastava.com/';

  dynamic report() async {
    var id = await box.read("class");
    try {
      print('Sending to ${_baseUrl}submissions/$id');
      Response response =
          await _dio.post('${_baseUrl}submissions/$id', data: {"class_id": id});

      print('Report: ${response.data}');
      return response.data as List<dynamic>;
    } catch (e) {
      print('Error getting classes: $e');
    }
  }
}
