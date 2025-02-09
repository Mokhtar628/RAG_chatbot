
import '../../domain/entities/chat.dart';

class ChatModel extends Chat {
  ChatModel({
    required String question,
    required String answer,
  }) : super(question: question, answer: answer);

  factory ChatModel.fromJson(Map<String, dynamic> json) {
    return ChatModel(
      question: json['question'] as String,
      answer: json['answer'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'question': question,
      'answer': answer,
    };
  }
}
