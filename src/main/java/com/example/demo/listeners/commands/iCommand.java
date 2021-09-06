package com.example.demo.listeners.commands;

import java.util.List;

public interface iCommand {
    void handle();
    String getName();

    default List<String> getAliases() {
        return List.of();
    }
}
