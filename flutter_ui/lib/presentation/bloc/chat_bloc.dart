import 'package:flutter_bloc/flutter_bloc.dart';
import 'chat_event.dart';
import 'chat_state.dart';
import '../../domain/entities/chat.dart';
import '../../domain/usecases/ask_chat_usecase.dart';

class ChatBloc extends Bloc<ChatEvent, ChatState> {
  final AskChatUseCase askChatUseCase;

  ChatBloc({required this.askChatUseCase})
      : super(ChatLoaded(chats: [])) {
    on<SendMessageEvent>(_onSendMessage);
  }

  Future<void> _onSendMessage(
      SendMessageEvent event, Emitter<ChatState> emit) async {

    final currentChats = state is ChatLoaded
        ? List<Chat>.from((state as ChatLoaded).chats)
        : <Chat>[];

    final userChat = Chat(question: event.message, answer: "");
    currentChats.add(userChat);

    final typingIndicator = Chat(question: "", answer: "typing");
    currentChats.add(typingIndicator);

    emit(ChatLoaded(chats: List.from(currentChats)));

    final result = await askChatUseCase(event.message);

    currentChats.removeWhere((chat) => chat.question == "" && chat.answer == "typing");

    emit(ChatLoaded(chats: List.from(currentChats)));

    result.fold(
          (failure) {
        currentChats.add(Chat(
          question: event.message,
          answer: "Sorry, an error occurred. Please try again.",
        ));
        emit(ChatLoaded(chats: List.from(currentChats)));
      },
          (chat) {
        currentChats.add(chat);
        emit(ChatLoaded(chats: List.from(currentChats)));
      },
    );
  }
}
