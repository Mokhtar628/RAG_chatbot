import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;

import 'presentation/bloc/chat_bloc.dart';
import 'presentation/pages/chat_page.dart';
import 'domain/usecases/ask_chat_usecase.dart';
import 'data/datasources/chat_remote_data_source.dart';
import 'data/repositories/chat_repository_impl.dart';

void main() {
  // Initialize dependencies
  final httpClient = http.Client();
  final chatRemoteDataSource = ChatRemoteDataSourceImpl(client: httpClient);
  final chatRepository = ChatRepositoryImpl(remoteDataSource: chatRemoteDataSource);
  final askChatUseCase = AskChatUseCase(chatRepository);

  runApp(MyApp(askChatUseCase: askChatUseCase));
}

class MyApp extends StatelessWidget {
  final AskChatUseCase askChatUseCase;

  const MyApp({Key? key, required this.askChatUseCase}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RAG Chat Bot',
      debugShowCheckedModeBanner: false,
      home: BlocProvider(
        create: (_) => ChatBloc(askChatUseCase: askChatUseCase),
        child: const ChatPage(),
      ),
    );
  }
}
