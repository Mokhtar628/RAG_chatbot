import 'package:dartz/dartz.dart';
import '../../core/errors/failures.dart';
import '../entities/chat.dart';

abstract class ChatRepository {
  Future<Either<Failure, Chat>> askQuestion(String question);
}
