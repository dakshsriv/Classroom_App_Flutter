import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:flutter/scheduler.dart';

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
    SchedulerBinding.instance.addPostFrameCallback((_) {
    Navigator.of(context).pushNamed("/login/");
});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
            appBar: AppBar(
                backgroundColor: Colors.blue,
                title: const Text("Classroom App")),
            body: Column(children: [
              Text("The user id is: $userID"),
              Text("The account type is: $accountType"),
            ])
        
    );
  }
}
