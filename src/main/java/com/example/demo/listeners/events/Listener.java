package com.example.demo.listeners.events;

import com.example.demo.listeners.CommandManager;
import com.example.demo.listeners.Config;
import me.duncte123.botcommons.BotCommons;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.events.ReadyEvent;
import net.dv8tion.jda.api.events.message.guild.GuildMessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.lang.NonNull;

import javax.annotation.Nonnull;


public class Listener extends ListenerAdapter {

    public static final Logger LOGGER = LoggerFactory.getLogger(Listener.class);
    private final CommandManager manager = new CommandManager();

    @Override
    public void onReady(@NonNull ReadyEvent event){
        LOGGER.info("Logged in as : "+ event.getJDA().getSelfUser()+"\nTotal Servers : "+ event.getJDA().getGuilds().size()+"\nBOT is Awake!");
    }

    @Override
    public void onGuildMessageReceived(@Nonnull GuildMessageReceivedEvent event) {
        User user = event.getAuthor();

        if (user.isBot() || event.isWebhookMessage()) {
            return;
        }

        String prefix = Config.get("PREFIX");
        String raw = event.getMessage().getContentRaw();

        if (raw.equalsIgnoreCase(prefix+"shutdown") && user.getId().equals(Config.get("OWNER_ID"))) {
            LOGGER.info("Shutting Down...");
            event.getJDA().shutdown();
            BotCommons.shutdown(event.getJDA());

            return;
        }
        if (raw.startsWith(prefix)) {
            manager.handle(event);
        }
    }
}
