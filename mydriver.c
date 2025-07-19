#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static int __init example_init(void) {
    printk(KERN_INFO "Example driver loaded.\n");
    return 0;
}

static void __exit example_exit(void) {
    printk(KERN_INFO "Example driver unloaded.\n");
}

module_init(example_init);
module_exit(example_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("A simple Linux device driver example.");
