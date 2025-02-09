using System.Threading.Tasks;
using Chatbot.Api.Models;
using Chatbot.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace Chatbot.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ChatController : ControllerBase
    {
        private readonly IChatService _chatService;
        public ChatController(IChatService chatService)
        {
            _chatService = chatService;
        }

        // POST: api/chat/ask
        [HttpPost("ask")]
        public async Task<IActionResult> Ask([FromBody] QueryRequest request)
        {
            if (string.IsNullOrWhiteSpace(request.Question))
            {
                return BadRequest("Question cannot be empty.");
            }

            QueryResponse response = await _chatService.ProcessQueryAsync(request);
            return Ok(response);
        }
    }
}
