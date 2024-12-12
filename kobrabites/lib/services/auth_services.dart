import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user_model.dart';

class AuthService {
  final String baseUrl = "http://localhost:8000/api";

  Future<UserModel> registerUser({
    required String email,
    required String username,
    required String password,
    required String firstName,
    required String lastName,
    String? phone,
    String? pronouns,
    String? gender,
    bool? emailOptIn,
    bool? phoneOptIn,
  }) async {
    final url = Uri.parse('$baseUrl/register/');
    final body = {
      "user": {
        "email": email,
        "username": username,
        "password": password
      },
      "first_name": firstName,
      "last_name": lastName,
      // Optional fields
      if (phone != null) "phone": phone,
      if (pronouns != null) "pronouns": pronouns,
      if (gender != null) "gender": gender,
      if (emailOptIn != null) "email_opt_in": emailOptIn,
      if (phoneOptIn != null) "phone_opt_in": phoneOptIn,
    };

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(body),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      return UserModel.fromJson(data);
    } else {
      throw Exception("Registration failed: ${response.statusCode} ${response.body}");
    }
  }

  Future<UserModel> loginUser(String email, String password) async {
    final url = Uri.parse('$baseUrl/login/');
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"email": email, "password": password}),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      return UserModel.fromJson(data);
    } else {
      throw Exception("Login failed: ${response.statusCode} ${response.body}");
    }
  }
}
