import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter_conditional_rendering/flutter_conditional_rendering.dart';

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
      userID = box.read('userID');
      accountType = box.read('accountType');
      print("userID: $userID, accountType: $accountType");
    } catch (e) {
      SchedulerBinding.instance.addPostFrameCallback((_) {
                Navigator.pushNamedAndRemoveUntil(context, "/login/", (_) => false);("/login/");

      });
    }
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
          Text("The user id is: $userID"),
          Text("The account type is: $accountType"),
          Column(children: [
            TextButton(
              onPressed: () {
                box.write("userID", "");
                box.write("accountType", "");
                        Navigator.pushNamedAndRemoveUntil(context, "/class_create/", (_) => false);("/login/");

              },
              child: const Text('Log out'),
            ),
            Conditional.single(
              context: context,
              conditionBuilder: (BuildContext context) =>
                  box.read('accountType') == "student",
              widgetBuilder: (BuildContext context) => Text('Student account'),
              fallbackBuilder: (BuildContext context) => Row(children: [
                Text('Teacher account!'),
                TextButton(
                  onPressed: () {
                    Navigator.pushNamed(context, "/class_create/");
                  },
                  child: const Text('Create a class'),
                )
              ]),
            ),
          ])
        ]));
  }
}
