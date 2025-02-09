import 'package:equatable/equatable.dart';
import '../../domain/entities/chat.dart';

abstract class ChatState extends Equatable {
  const ChatState();

  @override
  List<Object> get props => [];
}

class ChatInitial extends ChatState {}

class ChatLoading extends ChatState {}

class ChatLoaded extends ChatState {
  /// Contains all chat messages (both user and bot responses).
  final List<Chat> chats;

  const ChatLoaded({required this.chats});

  @override
  List<Object> get props => [chats];
}

class ChatError extends ChatState {
  final String message;

  const ChatError({required this.message});

  @override
  List<Object> get props => [message];
}
