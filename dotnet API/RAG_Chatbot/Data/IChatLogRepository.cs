using Chatbot.Api.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Chatbot.Api.Repositories
{
    public interface IChatLogRepository
    {
        Task SaveChatLogAsync(ChatLog chatLog);
    }
}
