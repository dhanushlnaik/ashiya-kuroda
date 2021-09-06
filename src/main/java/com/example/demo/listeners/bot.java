package com.example.demo.listeners;

import com.example.demo.listeners.events.Listener;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;

public class bot {


    public static void main(String args[]) throws Exception {
        JDA jda = JDABuilder.createDefault(Config.get("TOKEN")).build();
        jda.getPresence().setActivity(Activity.watching("Tatsui <3"));
        jda.addEventListener(new Listener());
    }
}
