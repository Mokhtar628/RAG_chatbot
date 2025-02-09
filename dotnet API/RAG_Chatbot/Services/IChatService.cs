using Chatbot.Api.Models;

namespace Chatbot.Api.Services
{
    public interface IChatService
    {
        Task<QueryResponse> ProcessQueryAsync(QueryRequest request);
    }
}
