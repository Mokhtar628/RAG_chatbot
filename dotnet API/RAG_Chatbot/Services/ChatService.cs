﻿using Chatbot.Api.Data;
using Chatbot.Api.Models;

namespace Chatbot.Api.Services
{
    public class ChatService : IChatService
    {
        private readonly IPythonBackendClient _pythonBackendClient;
        private readonly ChatbotDbContext _dbContext;

        public ChatService(IPythonBackendClient pythonBackendClient, ChatbotDbContext dbContext)
        {
            _pythonBackendClient = pythonBackendClient;
            _dbContext = dbContext;
        }

        public async Task<QueryResponse> ProcessQueryAsync(QueryRequest request)
        {
            QueryResponse response = await _pythonBackendClient.SendQueryAsync(request.Question);

            var chatLog = new ChatLog
            {
                UserId = "anonymous",  // Default until auth is implemented
                Question = request.Question,
                Answer = response.Answer
            };

            _dbContext.ChatLogs.Add(chatLog);
            await _dbContext.SaveChangesAsync();

            return response;
        }
    }
}
