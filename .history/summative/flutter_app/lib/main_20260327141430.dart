import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Student Exam Score Predictor',
      theme: ThemeData(primarySwatch: Colors.blue, useMaterial3: true),
      home: const PredictorScreen(),
    );
  }
}

class PredictorScreen extends StatefulWidget {
  const PredictorScreen({Key? key}) : super(key: key);

  @override
  State<PredictorScreen> createState() => _PredictorScreenState();
}

class _PredictorScreenState extends State<PredictorScreen> {
  final String apiBaseUrl = 'https://student-exam-predictor-v1.onrender.com';

  late TextEditingController hoursStudiedController;
  late TextEditingController attendanceController;
  late TextEditingController sleepHoursController;
  late TextEditingController previousScoresController;
  late TextEditingController tutorlingSessionsController;
  late TextEditingController physicalActivityController;

  String? selectedParentalInvolvement;
  String? selectedAccessToResources;
  String? selectedExtracurricular;
  String? selectedMotivation;
  String? selectedInternetAccess;
  String? selectedFamilyIncome;
  String? selectedTeacherQuality;
  String? selectedSchoolType;
  String? selectedPeerInfluence;
  String? selectedLearningDisabilities;
  String? selectedParentalEducation;
  String? selectedDistanceFromHome;

  double? predictedScore;
  bool isLoading = false;
  String? errorMessage;

  @override
  void initState() {
    super.initState();
    hoursStudiedController = TextEditingController();
    attendanceController = TextEditingController();
    sleepHoursController = TextEditingController();
    previousScoresController = TextEditingController();
    tutorlingSessionsController = TextEditingController();
    physicalActivityController = TextEditingController();
  }

  @override
  void dispose() {
    hoursStudiedController.dispose();
    attendanceController.dispose();
    sleepHoursController.dispose();
    previousScoresController.dispose();
    tutorlingSessionsController.dispose();
    physicalActivityController.dispose();
    super.dispose();
  }

  Future<void> predictScore() async {
    if (!_validateInputs()) {
      setState(() => errorMessage = 'Please fill all fields');
      return;
    }

    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final payload = {
        'Hours_Studied': int.parse(hoursStudiedController.text),
        'Attendance': int.parse(attendanceController.text),
        'Parental_Involvement': selectedParentalInvolvement,
        'Access_to_Resources': selectedAccessToResources,
        'Extracurricular_Activities': selectedExtracurricular,
        'Sleep_Hours': int.parse(sleepHoursController.text),
        'Previous_Scores': int.parse(previousScoresController.text),
        'Motivation_Level': selectedMotivation,
        'Internet_Access': selectedInternetAccess,
        'Tutoring_Sessions': int.parse(tutorlingSessionsController.text),
        'Family_Income': selectedFamilyIncome,
        'Teacher_Quality': selectedTeacherQuality,
        'School_Type': selectedSchoolType,
        'Peer_Influence': selectedPeerInfluence,
        'Physical_Activity': int.parse(physicalActivityController.text),
        'Learning_Disabilities': selectedLearningDisabilities,
        'Parental_Education_Level': selectedParentalEducation,
        'Distance_from_Home': selectedDistanceFromHome,
      };

      final response = await http
          .post(
            Uri.parse('$apiBaseUrl/predict'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode(payload),
          )
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          predictedScore = data['predicted_exam_score'].toDouble();
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Error: ${response.statusCode}';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Connection error: $e';
        isLoading = false;
      });
    }
  }

  bool _validateInputs() {
    return hoursStudiedController.text.isNotEmpty &&
        attendanceController.text.isNotEmpty &&
        sleepHoursController.text.isNotEmpty &&
        previousScoresController.text.isNotEmpty &&
        tutorlingSessionsController.text.isNotEmpty &&
        physicalActivityController.text.isNotEmpty &&
        selectedParentalInvolvement != null &&
        selectedAccessToResources != null &&
        selectedExtracurricular != null &&
        selectedMotivation != null &&
        selectedInternetAccess != null &&
        selectedFamilyIncome != null &&
        selectedTeacherQuality != null &&
        selectedSchoolType != null &&
        selectedPeerInfluence != null &&
        selectedLearningDisabilities != null &&
        selectedParentalEducation != null &&
        selectedDistanceFromHome != null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Student Exam Score Predictor'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            if (errorMessage != null)
              Container(
                padding: const EdgeInsets.all(12),
                margin: const EdgeInsets.only(bottom: 16),
                decoration: BoxDecoration(
                  color: Colors.red.shade50,
                  border: Border.all(color: Colors.red),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  errorMessage!,
                  style: TextStyle(color: Colors.red.shade700),
                ),
              ),
            if (predictedScore != null)
              Container(
                padding: const EdgeInsets.all(16),
                margin: const EdgeInsets.only(bottom: 16),
                decoration: BoxDecoration(
                  color: Colors.green.shade50,
                  border: Border.all(color: Colors.green),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  children: [
                    const Text(
                      'Predicted Exam Score',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      '${predictedScore!.toStringAsFixed(2)}%',
                      style: TextStyle(
                        fontSize: 36,
                        fontWeight: FontWeight.bold,
                        color: Colors.green.shade700,
                      ),
                    ),
                  ],
                ),
              ),
            TextField(
              controller: hoursStudiedController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Hours Studied (1-44)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: attendanceController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Attendance % (60-100)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedParentalInvolvement,
              hint: const Text('Parental Involvement'),
              items: [
                'Low',
                'Medium',
                'High',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedParentalInvolvement = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedAccessToResources,
              hint: const Text('Access to Resources'),
              items: [
                'Low',
                'Medium',
                'High',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedAccessToResources = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedExtracurricular,
              hint: const Text('Extracurricular Activities'),
              items: [
                'No',
                'Yes',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedExtracurricular = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: sleepHoursController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Sleep Hours (4-10)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: previousScoresController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Previous Scores (50-100)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedMotivation,
              hint: const Text('Motivation Level'),
              items: [
                'Low',
                'Medium',
                'High',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) => setState(() => selectedMotivation = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedInternetAccess,
              hint: const Text('Internet Access'),
              items: [
                'No',
                'Yes',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedInternetAccess = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: tutorlingSessionsController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Tutoring Sessions (0-8)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedFamilyIncome,
              hint: const Text('Family Income'),
              items: [
                'Low',
                'Medium',
                'High',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedFamilyIncome = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedTeacherQuality,
              hint: const Text('Teacher Quality'),
              items: [
                'Low',
                'Medium',
                'High',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedTeacherQuality = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedSchoolType,
              hint: const Text('School Type'),
              items: [
                'Public',
                'Private',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) => setState(() => selectedSchoolType = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedPeerInfluence,
              hint: const Text('Peer Influence'),
              items: [
                'Positive',
                'Neutral',
                'Negative',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedPeerInfluence = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: physicalActivityController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Physical Activity (0-6 hrs)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedLearningDisabilities,
              hint: const Text('Learning Disabilities'),
              items: [
                'No',
                'Yes',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedLearningDisabilities = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedParentalEducation,
              hint: const Text('Parental Education Level'),
              items: [
                'High School',
                'College',
                'Postgraduate',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedParentalEducation = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: selectedDistanceFromHome,
              hint: const Text('Distance from Home'),
              items: [
                'Near',
                'Moderate',
                'Far',
              ].map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) =>
                  setState(() => selectedDistanceFromHome = value),
              decoration: const InputDecoration(border: OutlineInputBorder()),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: isLoading ? null : predictScore,
              style: ElevatedButton.styleFrom(
                minimumSize: const Size.fromHeight(50),
              ),
              child: isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text(
                      'Predict Exam Score',
                      style: TextStyle(fontSize: 16),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
