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
            // Assuming the Python backend expects a JSON with a "question" property.
            var response = await _httpClient.PostAsJsonAsync("http://localhost:8000/ask", new { question });
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadFromJsonAsync<QueryResponse>();
        }
    }
}
