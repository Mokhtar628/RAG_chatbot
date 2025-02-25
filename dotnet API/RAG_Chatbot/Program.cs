using Chatbot.Api.Data;
using Chatbot.Api.Repositories;
using Chatbot.Api.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);


// Load configuration from appsettings.json
var pythonBackendUrl = builder.Configuration["PythonBackend:BaseUrl"]
                       ?? throw new InvalidOperationException("PythonBackend URL is missing.");

// Register HttpClient with the configured base URL
builder.Services.AddHttpClient<IPythonBackendClient, PythonBackendClient>(client =>
{
    client.BaseAddress = new Uri(pythonBackendUrl);
});

// Add services to the container.

builder.Services.AddControllers();

// Add CORS policy
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
        policy
            .AllowAnyOrigin()
            .AllowAnyMethod()
            .AllowAnyHeader());
});

// Configure EF Core with SQLite (adjust the connection string as needed)
builder.Services.AddDbContext<ChatbotDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));
builder.Services.AddScoped<IChatLogRepository, ChatLogRepository>();
builder.Services.AddScoped<IChatService, ChatService>();

// Register the Python backend client as a typed HttpClient.
builder.Services.AddHttpClient<IPythonBackendClient, PythonBackendClient>();

// Register our business logic service.
builder.Services.AddScoped<IChatService, ChatService>();

// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Apply any pending migrations and create the database if not exists.
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<ChatbotDbContext>();
    dbContext.Database.Migrate();
}

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseRouting();

// Enable CORS using the defined policy.
app.UseCors("AllowAll");

app.UseAuthorization();

app.MapControllers();

app.Run();
