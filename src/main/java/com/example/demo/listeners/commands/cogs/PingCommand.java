package com.example.demo.listeners.commands.cogs;

import com.example.demo.listeners.commands.CommandContext;
import com.example.demo.listeners.commands.iCommand;
import net.dv8tion.jda.api.JDA;

import java.util.List;

public class PingCommand implements iCommand {
    @Override
    public void handle(CommandContext ctx) {
        JDA jda = ctx.getJDA();

        jda.getRestPing().queue(
                (ping) -> ctx.getChannel()
                .sendMessageFormat("Rest Ping: %sms\nWS ping: %sms", ping,jda.getGatewayPing()).queue()
        );
    }

    @Override
    public String getName() {
        return "ping";
    }

    @Override
    public List<String> getAliases() {
        return null;
    }
}
