using System;

namespace Chatbot.Api.Models
{
    public class ChatLog
    {
        public int Id { get; set; }
        public string UserId { get; set; } = "anonymous"; // ToDO: Store the recieved id later
        public required string Question { get; set; }
        public required string Answer { get; set; }
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    }
}
