<template>
  <v-app>
    <v-app-bar>
      <v-container class="d-flex align-center py-0">
        <v-app-bar-title class="pl-0">
          <div class="d-flex align-center">
            <v-avatar
              class="me-3"
              image="https://cdn.vuetifyjs.com/docs/images/logos/v.png"
              rounded="0"
            />

            Vuetify 3
          </div>
        </v-app-bar-title>

        <v-spacer />

        <v-btn-alt
          append-icon="mdi-open-in-new"
          href="https://vuetifyjs.com/components/all/"
          rel="noopener noreferrer"
          target="_blank"
          text="Vuetify Documentation"
        />
      </v-container>
    </v-app-bar>

    <v-main>

    </v-main>

    <v-footer>
      <v-container class="text-overline d-flex align-center justify-space-between">
        <div>
          Copyright &copy; 2016-{{ (new Date()).getFullYear() }} Vuetify, LLC
        </div>

        <v-icon icon="$vuetify" size="x-large" />
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup>
  //
</script>
