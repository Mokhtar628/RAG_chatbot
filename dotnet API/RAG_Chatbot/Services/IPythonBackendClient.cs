using Chatbot.Api.Models;

namespace Chatbot.Api.Services
{
    public interface IPythonBackendClient
    {
        Task<QueryResponse> SendQueryAsync(string question);
    }
}
