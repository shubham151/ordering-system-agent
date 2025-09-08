<script lang="ts">
  import type { TotalCardProps } from '$lib/types';
  
  export let title: TotalCardProps['title'];
  export let value: TotalCardProps['value'];
  export let icon: TotalCardProps['icon'];
  export let color: TotalCardProps['color'];
  
  const colorClasses = {
    red: 'border-red-500',
    yellow: 'border-yellow-500',
    blue: 'border-blue-500'
  };
</script>

<div class="bg-white rounded-lg shadow-md p-6 border-l-4 {colorClasses[color]}">
  <div class="flex items-center justify-between">
    <div>
      <p class="text-sm font-medium text-gray-600">{title}</p>
      <p class="text-3xl font-bold text-gray-900">{value}</p>
    </div>
    <div class="text-4xl"><img src={icon} alt={title} class="w-10 h-10 object-contain" /></div>
  </div>
</div>