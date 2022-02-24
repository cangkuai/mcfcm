package cn.ckapp.fcm;
import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;


public final class Fcm extends JavaPlugin {

    @Override
    public void onEnable() {
        // Plugin startup logic
        getServer().getPluginManager().registerEvents(new chack(),this);
        if (Bukkit.getPluginCommand("chacks") != null) {
            Bukkit.getPluginCommand("chacks").setExecutor(new Commander());
        }
    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
    }
}
