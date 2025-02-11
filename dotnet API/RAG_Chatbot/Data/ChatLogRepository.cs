using Chatbot.Api.Data;
using Chatbot.Api.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Chatbot.Api.Repositories
{
    public class ChatLogRepository : IChatLogRepository
    {
        private readonly ChatbotDbContext _dbContext;

        public ChatLogRepository(ChatbotDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task SaveChatLogAsync(ChatLog chatLog)
        {
            _dbContext.ChatLogs.Add(chatLog);
            await _dbContext.SaveChangesAsync();
        }

    }
}
