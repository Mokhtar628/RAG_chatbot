using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using Chatbot.Api.Models;

namespace Chatbot.Api.Services
{
    public class PythonBackendClient : IPythonBackendClient
    {
        private readonly HttpClient _httpClient;
        public PythonBackendClient(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<QueryResponse> SendQueryAsync(string question)
        {
            var response = await _httpClient.PostAsJsonAsync("/ask", new { question });
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<QueryResponse>();
        }
    }
}
