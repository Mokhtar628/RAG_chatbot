using Chatbot.Api.Data;
using Chatbot.Api.Models;
using Chatbot.Api.Repositories;

namespace Chatbot.Api.Services
{
    public class ChatService : IChatService
    {
        private readonly IPythonBackendClient _pythonBackendClient;
        private readonly IChatLogRepository _chatLogRepository;

        public ChatService(IPythonBackendClient pythonBackendClient, IChatLogRepository chatLogRepository)
        {
            _pythonBackendClient = pythonBackendClient;
            _chatLogRepository = chatLogRepository;
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

            await _chatLogRepository.SaveChatLogAsync(chatLog);

            return response;
        }
    }
}
