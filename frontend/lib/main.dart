import 'package:flutter/material.dart';

void main() {
  runApp(const HomePage());
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
            appBar: AppBar(
              backgroundColor: Colors.blue,
              title: const Text("Classroom App"),
            ),
            body: Center(
                child: Row(children: [
              Text("$count"),
              FloatingActionButton(onPressed: () {
                setState(() {
                  count++;
                });
              })
            ]))));
  }
}
