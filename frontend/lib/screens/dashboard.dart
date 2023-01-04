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
  String userID = "";
  String accountType = "";

  @override
  void initState() {
    super.initState();
    try {
      userID = box.read("userID");
      accountType = box.read("accountType");
    }
    catch (e) {
      Navigator.pushNamed(context, "/login/");
    }
  }

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
