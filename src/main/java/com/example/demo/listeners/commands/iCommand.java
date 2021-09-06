package com.example.demo.listeners.commands;

import java.util.List;

public interface iCommand {
    void handle(CommandContext ctx);
    String getName();

    default List<String> getAliases() {
        return List.of();
    }
}
