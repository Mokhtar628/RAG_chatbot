namespace Chatbot.Api.Models
{
    public class QueryRequest
    {
        public required string Question { get; set; }
        //ToDo: add the userId, sessionId or whatever to store it after authentication
    }
}
