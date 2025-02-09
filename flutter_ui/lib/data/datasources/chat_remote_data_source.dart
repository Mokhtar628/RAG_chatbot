import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/errors/exceptions.dart';
import '../models/chat_model.dart';

abstract class ChatRemoteDataSource {
  /// Calls the API endpoint to get the answer for a given question.
  ///
  /// Throws a [ServerException] for all error codes.
  Future<ChatModel> askQuestion(String question);
}

class ChatRemoteDataSourceImpl implements ChatRemoteDataSource {
  final http.Client client;

  ChatRemoteDataSourceImpl({required this.client});

  @override
  Future<ChatModel> askQuestion(String question) async {
    final response = await client.post(
      Uri.parse('http://localhost:5042/api/Chat/ask'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'question': question}),
    );

    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');

    if (response.statusCode == 200) {
      final jsonMap = json.decode(response.body);
      return ChatModel.fromJson(jsonMap);
    } else {
      throw ServerException();
    }
  }
}
