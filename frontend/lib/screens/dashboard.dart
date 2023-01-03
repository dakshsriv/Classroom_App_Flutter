import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';

void main() async {
  await GetStorage.init();
  runApp(const Dashboard());
}

final box = GetStorage();

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}


class _DashboardState extends State<Dashboard> {
  String userID = box.read("userID");
  String accountType = box.read("accountType");

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
            appBar: AppBar(
                backgroundColor: Colors.blue,
                title: const Text("Classroom App")),
            body: Column(children: [
              Text("The user id is: $userID"),
              Text("The account type is: $accountType"),
            ])
        )
    );
  }
}
