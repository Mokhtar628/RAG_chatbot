import 'package:equatable/equatable.dart';

class Chat extends Equatable {
  final String question;
  final String answer;

  Chat({
    required this.question,
    required this.answer,
  });

  @override
  List<Object> get props => [question, answer];
}
