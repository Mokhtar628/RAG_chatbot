import 'package:flutter/material.dart';

class ChatBubbleTailClipper extends CustomClipper<Path> {
  final bool isUser;

  ChatBubbleTailClipper({required this.isUser});

  @override
  Path getClip(Size size) {
    final path = Path();
    if (isUser) {
      path.moveTo(size.width, 0);
      path.lineTo(size.width, size.height);
      path.lineTo(0, size.height);
    } else {
      path.moveTo(0, 0);
      path.lineTo(size.width, size.height);
      path.lineTo(size.width, 0);
    }
    return path;
  }

  @override
  bool shouldReclip(CustomClipper<Path> oldClipper) => false;
}