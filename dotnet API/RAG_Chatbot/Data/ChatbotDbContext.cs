using Chatbot.Api.Models;
using Microsoft.EntityFrameworkCore;


namespace Chatbot.Api.Data
{
    public class ChatbotDbContext : DbContext
    {
        public ChatbotDbContext(DbContextOptions<ChatbotDbContext> options)
            : base(options)
        {
        }
        public DbSet<ChatLog> ChatLogs { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<ChatLog>(entity =>
            {
                entity.HasKey(e => e.Id);
                entity.Property(e => e.Question).IsRequired();
                entity.Property(e => e.Answer).IsRequired();
                entity.Property(e => e.Timestamp)
                      .HasDefaultValueSql("CURRENT_TIMESTAMP");
            });
        }
    }
}
