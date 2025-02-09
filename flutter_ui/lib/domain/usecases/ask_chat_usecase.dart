import 'package:dartz/dartz.dart';
import '../../core/errors/failures.dart';
import '../entities/chat.dart';
import '../repositories/chat_repository.dart';

class AskChatUseCase {
  final ChatRepository repository;

  AskChatUseCase(this.repository);

  Future<Either<Failure, Chat>> call(String question) async {
    return await repository.askQuestion(question);
  }
}
