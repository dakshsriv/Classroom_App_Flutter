import 'package:flutter/material.dart';
import 'package:frontend/screens/login.dart';
import 'package:frontend/screens/register.dart';
import 'package:frontend/screens/dashboard.dart';
import 'package:frontend/screens/create_classroom.dart';
import 'package:frontend/screens/classroom.dart';
import 'package:frontend/screens/edit_classroom.dart';


void main() async {
  runApp(const Main());
}

class Main extends StatelessWidget {
  const Main({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Named Routes Demo',
      // Start the app with the "/" named route. In this case, the app starts
      // on the FirstScreen widget.
      initialRoute: '/login/',
      routes: {
        // When navigating to the "/" route, build the FirstScreen widget.
        '/': (context) => const Dashboard(),
        // When navigating to the "/second" route, build the SecondScreen widget.
        '/login/': (context) => const LoginPage(),
        '/register/': (context) => const RegisterPage(),
        '/class_create/': (context) => const CreateClassroomPage(),
        '/classroom/': (context) => const Classroom(),
        '/class_edit/': (context) => const EditClassroomPage(),
      },
    );
  }
}
